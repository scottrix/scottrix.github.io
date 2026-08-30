"""Generate A-Level revision and lesson content for the standalone alevel repos.

Emits ONE collapsed topic page per unique topic (board-agnostic) at
    topics/{subject}/{topic-slug}.html
with a "Board differences" section, plus 301 redirects from the old per-board
pages (topics/{subject}/{board}/{topic}.html) to the collapsed page.
"""  # noqa: E501
import json, os, html, re

ROOT = '/home/scott/src'
BOARDS = ["AQA", "Edexcel", "OCR", "WJEC", "CCEA"]

# Each subject: name + topics. Each topic: title, objectives[], key[], example,
# answer, practice[]. The learning content is shared across boards; genuine
# differences between boards live in BOARD_DIFFERENCES below.
SUBJECTS = [
  {
    "name": "Mathematics",
    "topics": [
      {"title": "Algebraic Expressions", "objectives": ["Simplify algebraic expressions", "Expand brackets", "Factorise quadratic expressions"],
       "key": ["Collecting like terms", "Difference of two squares", "Factorising by grouping"],
       "example": "Simplify (2x + 3)(x - 4)", "answer": "2x² - 5x - 12",
       "practice": ["Expand (x + 5)(x - 2)", "Factorise x² + 6x + 9", "Simplify (3a²b)(4ab³)"]},
      {"title": "Quadratic Equations", "objectives": ["Solve by factorising", "Complete the square", "Use the quadratic formula"],
       "key": ["Factorising when a=1", "Completing the square (x + p)² + q", "Quadratic formula x = (−b ± √(b²−4ac)) / 2a"],
       "example": "Solve x² - 5x + 6 = 0", "answer": "x = 2 or x = 3",
       "practice": ["Solve 2x² + 7x + 3 = 0", "Complete the square for x² + 4x - 5", "Use the quadratic formula for 3x² - x - 2 = 0"]},
      {"title": "Coordinate Geometry", "objectives": ["Find the equation of a line", "Compute distance and midpoint", "Handle parallel and perpendicular lines"],
       "key": ["Gradient m = (y₂−y₁)/(x₂−x₁)", "Line y = mx + c", "Distance √((x₂−x₁)²+(y₂−y₁)²)", "Midpoint ((x₁+x₂)/2,(y₁+y₂)/2)"],
       "example": "Find the equation of the line through (1,2) and (3,6)", "answer": "y = 2x",
       "practice": ["Find line through (0,0) and (2,5)", "Are y=2x+1 and y=2x−3 parallel?", "Find intersection of y=x+1 and y=−x+3"]},
      {"title": "Differentiation", "objectives": ["Differentiate polynomials", "Find gradients and stationary points", "Apply the second derivative test"],
       "key": ["Power rule d/dx(xⁿ)=nxⁿ⁻¹", "Stationary point where f′(x)=0", "Second derivative classifies max/min"],
       "example": "Differentiate y = 3x⁴ - 2x³ + x", "answer": "dy/dx = 12x³ - 6x² + 1",
       "practice": ["Differentiate x⁵ - 4x³", "Find stationary points of y = x³ - 3x", "Classify with the second derivative"]},
      {"title": "Integration", "objectives": ["Integrate polynomials", "Evaluate definite integrals", "Find area under a curve"],
       "key": ["Increase power by 1 then divide", "∫axⁿ dx = axⁿ⁺¹/(n+1) + C", "∫ₐᵇ f(x)dx = F(b)−F(a)"],
       "example": "Integrate ∫(2x³ - 5x) dx", "answer": "x⁴/2 - 5x²/2 + C",
       "practice": ["∫(4x² + 3x) dx", "Evaluate ∫₀² (x² + 1) dx", "Area under y = x from x=0 to x=3"]},
      {"title": "Trigonometry", "objectives": ["Use sine and cosine rules", "Sketch trig graphs", "Solve trig equations"],
       "key": ["SOH CAH TOA", "sin²θ + cos²θ = 1", "Graph period and amplitude"],
       "example": "Solve sinθ = √3/2 for 0 ≤ θ < 2π", "answer": "θ = π/3, 2π/3",
       "practice": ["Solve cosθ = −1/2", "Sketch y = 2 sin x for 0≤x≤2π", "Find a side using the sine rule"]},
    ],
  },
  {
    "name": "Further Mathematics",
    "topics": [
      {"title": "Complex Numbers", "objectives": ["Work with complex arithmetic", "Represent numbers on the Argand diagram", "Solve polynomial equations with complex roots"],
       "key": ["z = a + bi", "Conjugate z̄ = a − bi", "Argand diagram and modulus/argument", "Roots of quadratics come in conjugate pairs"],
       "example": "Solve z² + 4 = 0", "answer": "z = ±2i",
       "practice": ["Add 3+4i and 5−2i", "Multiply (2+i)(3−i)", "Solve z² + 2z + 5 = 0"]},
      {"title": "Matrices", "objectives": ["Add and multiply matrices", "Compute determinants and inverses", "Solve systems with matrices"],
       "key": ["Matrix multiplication is non-commutative", "det(A) for 2x2 = ad−bc", "A⁻¹ = (1/det) adj(A)"],
       "example": "Find determinant of [[2,3],[1,4]]", "answer": "8 − 3 = 5",
       "practice": ["Multiply [[1,2],[3,4]] by [[5],[6]]", "Find the inverse of [[2,0],[0,3]]", "Solve 2x+3y=5, y=1 using matrices"]},
      {"title": "Vectors", "objectives": ["Use vector arithmetic and notation", "Compute scalar and vector products", "Work with lines in 3D"],
       "key": ["Position vectors r = a + λb", "Dot product for angle cosθ = (a·b)/(|a||b|)", "Scalar product of perpendicular vectors is zero"],
       "example": "Find cosθ between (1,2) and (3,4)", "answer": "(1·3+2·4)/(√5·5) = 11/(5√5)",
       "practice": ["Dot (2,−1,3) with (1,0,2)", "Are (1,2) and (−4,2) perpendicular?", "Write the line through two points in vector form"]},
      {"title": "Polar Coordinates", "objectives": ["Convert between polar and Cartesian", "Sketch simple polar curves", "Find areas in polar form"],
       "key": ["x = r cosθ, y = r sinθ", "r² = x² + y²", "Area = ½∫r² dθ"],
       "example": "Convert r = 2 to Cartesian", "answer": "x² + y² = 4 (a circle)",
       "practice": ["Convert (2, π/3) to Cartesian", "Sketch r = 2 cosθ", "Area enclosed by r = 3 from 0 to π"]},
      {"title": "Hyperbolic Functions", "objectives": ["Define sinh, cosh, tanh", "Use their identities", "Solve simple hyperbolic equations"],
       "key": ["sinh x = (eˣ − e⁻ˣ)/2", "cosh x = (eˣ + e⁻ˣ)/2", "cosh²x − sinh²x = 1"],
       "example": "Evaluate cosh 0", "answer": "cosh 0 = 1",
       "practice": ["Show cosh²x − sinh²x = 1", "Solve sinh x = 2", "Evaluate tanh x for large x"]},
    ],
  },
  {
    "name": "Physics",
    "topics": [
      {"title": "Mechanics and Motion", "objectives": ["Use SUVAT equations", "Apply Newton's laws", "Work with momentum and energy"],
       "key": ["v = u + at, s = ut + ½at²", "F = ma", "p = mv, KE = ½mv²", "Conservation of momentum"],
       "example": "A car accelerates from rest at 2 m/s² for 5 s. Distance?", "answer": "s = ½(2)(25) = 25 m",
       "practice": ["A ball falls from 20 m for 2 s, find its speed", "Force of 6 N on a 2 kg mass, find acceleration", "Two balls collide, find final momentum"]},
      {"title": "Electricity and Circuits", "objectives": ["Apply Ohm's law", "Combine resistors in series and parallel", "Work with power and energy"],
       "key": ["V = IR", "Series R = R₁+R₂, parallel 1/R = 1/R₁+1/R₂", "P = IV = I²R"],
       "example": "Current through a 6 V, 12 Ω lamp?", "answer": "I = 6/12 = 0.5 A",
       "practice": ["Two 4 Ω resistors in series, total resistance?", "Power of a 2 A device at 12 V", "Voltage across a 3 Ω resistor carrying 2 A"]},
      {"title": "Waves", "objectives": ["Describe wave properties", "Use the wave equation", "Apply the Doppler effect"],
       "key": ["v = fλ", "Longitudinal vs transverse", "Doppler shift Δf = f·v/c"],
       "example": "Speed of a wave with f = 50 Hz and λ = 6 m?", "answer": "v = 50 × 6 = 300 m/s",
       "practice": ["Find λ if v=340 m/s and f=100 Hz", "Is light transverse or longitudinal?", "Describe how frequency changes for a moving source"]},
      {"title": "Particles and Quantum Physics", "objectives": ["Describe fundamental particles", "Detect radiation", "Apply the photon model"],
       "key": ["Photon energy E = hf", "Quarks and leptons", "Radioactive decay and halflife"],
       "example": "Energy of a photon with f = 10¹⁵ Hz (h = 6.63×10⁻³⁴)", "answer": "E = 6.63×10⁻¹⁹ J",
       "practice": ["Find f of a photon with E = 3.3×10⁻¹⁹ J", "Name two leptons", "How many half-lives for 1/8 to remain?"]},
      {"title": "Thermal Physics", "objectives": ["Explain temperature and heat", "Use specific heat capacity", "Apply the gas laws"],
       "key": ["Q = mcΔθ", "Ideal gas PV = nRT", "Kinetic theory and absolute zero"],
       "example": "Heat to raise 2 kg of water by 10 K (c=4200 J/kgK)?", "answer": "Q = 2 × 4200 × 10 = 84 kJ",
       "practice": ["Heat to melt 0.5 kg of ice (specific latent heat 334 kJ/kg)", "State units of R", "Explain temperature in kinetic terms"]},
    ],
  },
  {
    "name": "Chemistry",
    "topics": [
      {"title": "Atomic Structure and Bonding", "objectives": ["Describe atomic structure", "Explain ionic and covalent bonding", "Use electronegativity"],
       "key": ["Protons, neutrons, electrons", "Ionic vs covalent bonds", "Electronegativity trends across the period"],
       "example": "Number of protons in carbon-14?", "answer": "6 (atomic number is 6)",
       "practice": ["State the charge of a neutron", "Give an example of an ionic compound", "Which element is most electronegative?"]},
      {"title": "Energetics", "objectives": ["Define enthalpy changes", "Use Hess's law", "Compute bond enthalpies"],
       "key": ["Enthalpy change ΔH", "Hess's law: path independent", "ΔH = Σ(bonds broken) − Σ(bonds formed)"],
       "example": "Is an exothermic reaction ΔH positive or negative?", "answer": "Negative (heat released)",
       "practice": ["Define standard enthalpy of formation", "Sketch an exothermic energy profile", "Compute ΔH from bond energies"]},
      {"title": "Kinetics and Equilibria", "objectives": ["Explain factors affecting rate", "Understand activation energy", "Apply Le Chatelier's principle"],
       "key": ["Rate ∝ concentration collisions", "Catalyst lowers activation energy", "Le Chatelier: equilibrium shifts to oppose change"],
       "example": "Effect of increasing temperature on equilibrium?", "answer": "Shifts in the endothermic direction",
       "practice": ["How does a catalyst affect equilibrium position?", "Explain why increasing concentration raises rate", "State what activation energy is"]},
      {"title": "Organic Chemistry", "objectives": ["Name organic compounds", "Identify functional groups", "Understand reaction mechanisms"],
       "key": ["Alkanes, alkenes, alcohols, carboxylic acids", "Naming rules (IUPAC)", "Substitution and addition reactions"],
       "example": "Functional group of an alcohol?", "answer": "−OH (hydroxyl)",
       "practice": ["Name CH₃CH₂CH₃", "Draw the structure of ethanol", "What type of reaction is an addition reaction?"]},
      {"title": "Redox and Electrochemistry", "objectives": ["Assign oxidation states", "Balance redox equations", "Use electrochemical series"],
       "key": ["Oxidation number rules", "Redox = reduction and oxidation", "Standard electrode potentials"],
       "example": "Oxidation state of Mn in MnO₄⁻?", "answer": "+7",
       "practice": ["Assign oxidation states in H₂O", "Balance Zn → Zn²⁺ + 2e⁻", "Which metal is more reactive in the series?"]},
    ],
  },
  {
    "name": "Biology",
    "topics": [
      {"title": "Cell Structure and Function", "objectives": ["Describe cell organelles", "Compare prokaryotic and eukaryotic cells", "Understand membrane transport"],
       "key": ["Nucleus, mitochondria, ribosomes", "Prokaryotes lack a nucleus", "Diffusion, osmosis, active transport"],
       "example": "Which organelle carries out respiration?", "answer": "Mitochondria",
       "practice": ["Name the organelle for protein synthesis", "List two differences between plant and animal cells", "Define osmosis"]},
      {"title": "Genetics and Inheritance", "objectives": ["Explain DNA structure and replication", "Use Punnett squares", "Describe gene expression"],
       "key": ["DNA double helix, base pairing", "Alleles, dominant and recessive", "Punnett squares predict ratios"],
       "example": "For a cross of two heterozygotes (Aa x Aa), phenotypic ratio?", "answer": "3:1 dominant to recessive",
       "practice": ["State the bases that pair with A and C", "Define genotype vs phenotype", "Use a Punnett square for Aa x aa"]},
      {"title": "Biochemistry and Respiration", "objectives": ["Describe the biochemistry of respiration", "Understand enzymes", "Explain the electron transport chain"],
       "key": ["Glycolysis, Krebs cycle", "ATP as energy currency", "Enzymes lower activation energy"],
       "example": "Where does glycolysis occur?", "answer": "In the cytoplasm",
       "practice": ["Name the products of glycolysis", "What is the role of ATP?", "Define active site"]},
      {"title": "Ecology and Ecosystems", "objectives": ["Describe energy flow through ecosystems", "Understand nutrient cycles", "Explain population dynamics"],
       "key": ["Trophic levels and food chains", "Carbon and nitrogen cycles", "Carrying capacity"],
       "example": "What happens to energy at each trophic level?", "answer": "Some is lost as heat, so less is available",
       "practice": ["Name two greenhouse gases", "Describe the carbon cycle in three steps", "Define a trophic level"]},
      {"title": "Homeostasis and the Nervous System", "objectives": ["Explain homeostasis", "Describe the nervous system", "Understand hormonal control"],
       "key": ["Negative feedback maintains balance", "Neurones transmit impulses", "Hormones travel in the blood"],
       "example": "What controls blood glucose?", "answer": "Insulin (and glucagon)",
       "practice": ["Define homeostasis", "Name the parts of a neurone", "What is the role of adrenaline?"]},
    ],
  },
  {
    "name": "English Literature",
    "topics": [
      {"title": "Poetry Analysis", "objectives": ["Analyse language and imagery", "Understand form and structure", "Compare poems"],
       "key": ["Metaphor, simile, personification", "Rhyme, rhythm, stanza", "Themes and personal response", "Compare across the anthology"],
       "example": "What effect does a metaphor create?", "answer": "It creates a vivid comparison that deepens meaning",
       "practice": ["Identify three poetic techniques in a given poem", "Discuss how structure affects meaning", "Compare two poems on a shared theme"]},
      {"title": "Prose and the Novel", "objectives": ["Analyse characters and themes", "Understand narrative voice", "Contextualise the novel"],
       "key": ["Character development", "Narrator and point of view", "Social and historical context"],
       "example": "How does the narrator shape the reader's view?", "answer": "Through biased or limited narration that guides sympathy",
       "practice": ["Trace a theme across a novel", "Explain the role of the setting", "Discuss how context influences meaning"]},
      {"title": "Drama and Shakespeare", "objectives": ["Analyse dramatic techniques", "Interpret Shakespearean language", "Evaluate staging and performance"],
       "key": ["Soliloquy, aside, dramatic irony", "Iambic pentameter, blank verse", "Stage directions and staging choices"],
       "example": "Why does Shakespeare use soliloquy?", "answer": "To reveal a character's private thoughts directly to the audience",
       "practice": ["Explain the effect of dramatic irony", "Analyse a key soliloquy", "Discuss how staging conveys theme"]},
      {"title": "Critical Writing and Context", "objectives": ["Structure a critical essay", "Use textual evidence", "Link text to wider context"],
       "key": ["Thesis-led paragraphs (PEEL)", "Quotation analysis not quotation dumping", "Context, author's intent, reader response"],
       "example": "How should an exam essay be structured?", "answer": "Introduction stating a thesis, developed points with evidence, conclusion",
       "practice": ["Write a topic sentence for a thesis", "Analyse a short quotation closely", "Link a novel to its historical context"]},
    ],
  },
  {
    "name": "History",
    "topics": [
      {"title": "Interpretation and Sources", "objectives": ["Evaluate historical sources", "Understand historical interpretations", "Build arguments from evidence"],
       "key": ["Primary vs secondary sources", "Utility and reliability", "Different interpretations of events"],
       "example": "Why are two historians' accounts different?", "answer": "Different evidence, perspectives, or historiographical schools",
       "practice": ["Assess the reliability of a source", "Compare two interpretations of a war", "Explain why sources disagree"]},
      {"title": "Themed Study: Key Eras", "objectives": ["Explain causes and consequences", "Identify turning points", "Evaluate change and continuity"],
       "key": ["Causes and consequences of events", "Turning points and significance", "Change vs continuity over time"],
       "example": "Why is an event a 'turning point'?", "answer": "It leads to significant, lasting change in society or policy",
       "practice": ["List causes of a key event", "Describe a major consequence", "Compare two periods for change and continuity"]},
      {"title": "Depth Study: a Period in Detail", "objectives": ["Explain detailed chronology", "Analyse key figures", "Assess significance"],
       "key": ["Chronology of events", "Key individuals and their impact", "Short-term vs long-term significance"],
       "example": "How significant was a single ruler?", "answer": "Assess personal impact against wider structural forces",
       "practice": ["Give a timeline of 5 key events", "Evaluate one leader's role", "Weigh short vs long-term significance"]},
      {"title": "Historical Enquiry and Essay Skills", "objectives": ["Plan a focused inquiry", "Use evidence effectively", "Write balanced conclusions"],
       "key": ["Framing a historical question", "Evidence weighting", "Balance and judgement in conclusions"],
       "example": "What makes a good conclusion?", "answer": "A justified judgement supported by the strongest evidence",
       "practice": ["Formulate an inquiry question", "Select two pieces of strong evidence", "Write a balanced judgement"]},
    ],
  },
  {
    "name": "Geography",
    "topics": [
      {"title": "Physical Geography", "objectives": ["Explain coastal processes", "Describe plate tectonics", "Understand river systems"],
       "key": ["Erosion, deposition, transportation", "Plate boundaries and hazards", "Drainage basins and flooding"],
       "example": "Name a coastal erosional landform", "answer": "Cliffs, headlands, bays, arches, stacks",
       "practice": ["Describe how an arch forms", "Explain the impact of a plate boundary", "List causes of flooding in a river basin"]},
      {"title": "Human Geography", "objectives": ["Explain urbanisation", "Analyse population change", "Understand development"],
       "key": ["Urbanisation and counterurbanisation", "Population pyramids and migration", "Indicators of development"],
       "example": "Define urbanisation", "answer": "The increasing proportion of people living in towns and cities",
       "practice": ["Explain why migration happens", "Interpret an age-sex pyramid", "State two measures of development"]},
      {"title": "Fieldwork and Data Collection", "objectives": ["Design fieldwork methods", "Collect and record data", "Analyse results"],
       "key": ["Hypotheses and methods", "Sampling techniques", "Data presentation (graphs, maps)"],
       "example": "Why use systematic sampling?", "answer": "To reduce bias and get representative data",
       "practice": ["Write a hypothesis", "Describe a sampling method", "Choose a suitable graph for data"]},
      {"title": "Hazards and Global Issues", "objectives": ["Explain natural hazards", "Analyse climate change impacts", "Evaluate management strategies"],
       "key": ["Tectonic and climatic hazards", "Vulnerability and resilience", "Adaptation and mitigation"],
       "example": "What is mitigation in climate change?", "answer": "Actions to reduce the causes, e.g. cutting emissions",
       "practice": ["Classify a hazard as tectonic or climatic", "Explain a climate change impact", "Evaluate one mitigation strategy"]},
    ],
  },
  {
    "name": "Economics",
    "topics": [
      {"title": "Microeconomics and Markets", "objectives": ["Explain supply and demand", "Analyse market equilibrium", "Understand elasticity"],
       "key": ["Demand and supply curves", "Equilibrium price and quantity", "Price elasticity of demand = %ΔQd/%ΔP"],
       "example": "What happens to price when supply rises?", "answer": "Price falls if demand is unchanged",
       "practice": ["Draw shifts in demand", "Calculate PED", "Explain the effect of a price ceiling"]},
      {"title": "Macroeconomics", "objectives": ["Measure economic growth", "Explain inflation and unemployment", "Use fiscal and monetary policy"],
       "key": ["GDP as a measure of output", "Inflation = sustained price rise", "Fiscal (tax/spending) and monetary (interest rates) policy"],
       "example": "Name a cost of inflation", "answer": "Reduced purchasing power / uncertainty",
       "practice": ["Define GDP", "Explain why unemployment matters", "Give an example of fiscal policy"]},
      {"title": "Market Failure and Government Intervention", "objectives": ["Identify types of market failure", "Explain externalities", "Evaluate government policies"],
       "key": ["Public goods, externalities, monopoly", "Negative and positive externalities", "Taxes, subsidies, regulation"],
       "example": "What is a negative externality?", "answer": "A cost to a third party, e.g. pollution",
       "practice": ["Give an example of a public good", "Explain how a tax corrects pollution", "Evaluate a subsidy"]},
      {"title": "International Trade and Development", "objectives": ["Explain comparative advantage", "Analyse globalisation", "Understand development indicators"],
       "key": ["Comparative advantage", "Free trade and protectionism", "Exchange rates"],
       "example": "Why do countries trade?", "answer": "To specialise and gain from comparative advantage",
       "practice": ["Explain an exchange rate change effect", "Describe a benefit of free trade", "State a development indicator"]},
    ],
  },
  {
    "name": "Business Studies",
    "topics": [
      {"title": "Marketing", "objectives": ["Segment markets", "Use the marketing mix", "Analyse pricing strategies"],
       "key": ["Market segmentation", "The 4 Ps: Product, Price, Place, Promotion", "Pricing strategies"],
       "example": "Define market segmentation", "answer": "Dividing a market into groups with common needs",
       "practice": ["Segment a phone market", "Explain the marketing mix", "Compare pricing strategies"]},
      {"title": "Finance and Accounts", "objectives": ["Interpret financial statements", "Calculate profitability", "Manage cash flow"],
       "key": ["Profit = revenue − costs", "Break-even point", "Liquidity and cash flow"],
       "example": "Profit if revenue £10k, costs £6k?", "answer": "£4k",
       "practice": ["Calculate gross profit", "Work out the break-even quantity", "Explain the importance of cash flow"]},
      {"title": "Operations Management", "objectives": ["Explain production methods", "Manage quality", "Understand supply chains"],
       "key": ["Job, batch, flow production", "Quality control and assurance", "Lean production"],
       "example": "Define lean production", "answer": "Minimising waste to improve efficiency",
       "practice": ["Compare job and flow production", "Explain total quality management", "State a benefit of good stock control"]},
      {"title": "People and Leadership", "objectives": ["Explain motivation theories", "Describe leadership styles", "Manage recruitment"],
       "key": ["Maslow and Herzberg", "Autocratic, democratic, laissez-faire", "Recruitment and selection process"],
       "example": "Name one motivator", "answer": "Recognition, achievement, autonomy, pay",
       "practice": ["Apply Maslow's hierarchy to a firm", "Compare leadership styles", "List recruitment stages"]},
      {"title": "Strategy and the External Environment", "objectives": ["Use SWOT and PESTEL", "Analyse competition", "Evaluate growth strategies"],
       "key": ["SWOT and PESTEL analysis", "Competitive advantage", "Organic vs inorganic growth"],
       "example": "What does SWOT stand for?", "answer": "Strengths, Weaknesses, Opportunities, Threats",
       "practice": ["Build a SWOT for a firm", "Explain a PESTEL factor", "Compare organic and inorganic growth"]},
    ],
  },
  {
    "name": "Computer Science",
    "topics": [
      {"title": "Programming Fundamentals", "objectives": ["Use variables and data types", "Control program flow", "Write functions"],
       "key": ["Integer, float, string, boolean", "If/else and loops", "Functions and parameters"],
       "example": "What data type stores true/false?", "answer": "Boolean",
       "practice": ["Write a loop to print 1-5", "Declare a string variable", "Write a function that adds two numbers"]},
      {"title": "Data Structures and Algorithms", "objectives": ["Use arrays and lists", "Trace search and sort algorithms", "Analyse complexity"],
       "key": ["Arrays and linked lists", "Linear/binary search, bubble/merge sort", "Big-O notation"],
       "example": "Which search is faster on sorted data?", "answer": "Binary search (O(log n) vs O(n))",
       "practice": ["Trace a binary search", "Describe a bubble sort pass", "State the complexity of linear search"]},
      {"title": "Computer Systems and Architecture", "objectives": ["Explain the CPU and fetch-decode-execute cycle", "Understand memory", "Describe storage"],
       "key": ["ALU, CU, registers", "RAM vs ROM", "Virtual memory and cache"],
       "example": "What does the ALU do?", "answer": "Performs arithmetic and logic operations",
       "practice": ["Order the FDE cycle steps", "Compare RAM and ROM", "Why is cache used?"]},
      {"title": "Networks and Internet", "objectives": ["Explain network topologies", "Understand protocols", "Describe cybersecurity threats"],
       "key": ["LAN vs WAN, topology", "TCP/IP, HTTP, DNS", "Malware, phishing, encryption"],
       "example": "What does HTTP do?", "answer": "Transfers web pages over the internet",
       "practice": ["Compare topologies", "Explain the role of DNS", "Name two cyber threats"]},
      {"title": "Boolean Logic and Relational Databases", "objectives": ["Use logic gates", "Normalise databases", "Query with SQL"],
       "key": ["AND, OR, NOT gates", "Entities, attributes, primary keys", "SELECT, FROM, WHERE"],
       "example": "Output of AND gate with inputs 1 and 0?", "answer": "0",
       "practice": ["Draw a truth table for OR", "Define a primary key", "Write a basic SQL SELECT query"]},
    ],
  },
  {
    "name": "Psychology",
    "topics": [
      {"title": "Approaches and Perspectives", "objectives": ["Compare psychological approaches", "Evaluate the biological approach", "Understand behaviourism"],
       "key": ["Biological, cognitive, behaviourist, psychodynamic, humanistic", "Nature vs nurture", "Determinism vs free will"],
       "example": "What does the biological approach focus on?", "answer": "Genes, brain structure and neurotransmitters",
       "practice": ["Outline behaviourism", "Evaluate the cognitive approach", "Explain the nature-nurture debate"]},
      {"title": "Research Methods", "objectives": ["Design experiments", "Use sampling techniques", "Analyse data"],
       "key": ["Independent and dependent variables", "Random and stratified sampling", "Measures of central tendency"],
       "example": "What is the independent variable?", "answer": "The variable the researcher manipulates",
       "practice": ["Write a hypothesis", "Describe random sampling", "State the mode of a data set"]},
      {"title": "Memory and Cognitive Psychology", "objectives": ["Explain multi-store model", "Describe short and long-term memory", "Understand forgetting"],
       "key": ["Sensory, short-term, long-term memory", "Capacity and duration", "Forgetting: interference and decay"],
       "example": "Typical capacity of short-term memory?", "answer": "7 ± 2 items",
       "practice": ["Outline the multi-store model", "Describe a forgetting theory", "Give an example of interference"]},
      {"title": "Social Influence and Attachment", "objectives": ["Explain conformity and obedience", "Describe types of attachment", "Evaluate research studies"],
       "key": ["Conformity and obedience", "Secure and insecure attachment", "Evaluation of key studies"],
       "example": "What is conformity?", "answer": "Changing behaviour to match the group",
       "practice": ["Give an example of obedience", "Describe secure attachment", "Evaluate a famous study"]},
      {"title": "Psychopathology", "objectives": ["Define abnormality", "Explain mental disorders", "Evaluate treatments"],
       "key": ["Statistical and social norms definitions", "Phobias, depression, OCD", "Biological and psychological treatments"],
       "example": "What is a phobia?", "answer": "An irrational, persistent fear of an object or situation",
       "practice": ["Define clinical depression", "Name a behavioural treatment for phobias", "Evaluate a biological treatment"]},
    ],
  },
]

def slug(t):
    return t.lower().replace(" ", "-").replace("/", "-")

def title_from_html(path):
    """Extract the <title> and strip the trailing site suffix for display."""
    try:
        with open(path, encoding='utf-8') as f:
            head = f.read(2000)
        m = re.search(r'<title>(.*?)</title>', head, re.IGNORECASE | re.DOTALL)
        if not m:
            return None
        t = m.group(1).strip()
        t = re.sub(r'\s*-\s*A-Level\s+.*$', '', t)
        t = re.sub(r'\s*[-–]\s*(Revision|Lessons)?\s*Notes?\s*$', '', t).strip()
        return t
    except OSError:
        return None

def flat_general_board(base, subject_name, mode, exclude_slugs=frozenset()):
    """Scan topics/{slug}/ for orphaned rich flat topic .html files (not board
    subdirs) and return them as a flat topics list (board-agnostic). These are
    single-subject rich pages and carry no board differences. Any slugs already
    written by the collapsed generator must be excluded so they are not listed
    twice."""
    tdir = os.path.join(base, "topics", slug(subject_name))
    entries = []
    if not os.path.isdir(tdir):
        return None
    for fn in sorted(os.listdir(tdir)):
        p = os.path.join(tdir, fn)
        if not (fn.endswith('.html') and os.path.isfile(p)):
            continue
        if fn[:-5] in exclude_slugs:
            continue
        display = title_from_html(p)
        if not display:
            display = fn[:-5].replace('-', ' ').title()
        entries.append({
            "title": display,
            "learningObjectives": [],
            "keyPoints": [],
            "exampleQuestion": "",
            "modelAnswer": "",
            "practiceQuestions": [],
            "page": f"topics/{slug(subject_name)}/{fn}",
            "boardDifferences": [],
        })
    if not entries:
        return None
    return entries


# Subject -> category (drives the home-page tabs). Matches regenerate_all.py.
CATEGORIES = {
  "Mathematics": "Core",
  "Further Mathematics": "Core",
  "English Literature": "Core",
  "English Language": "Core",
  "Biology": "Sciences",
  "Chemistry": "Sciences",
  "Physics": "Sciences",
  "Computer Science": "Sciences",
  "Economics": "Social Sciences",
  "Psychology": "Social Sciences",
  "Sociology": "Social Sciences",
  "Business Studies": "Social Sciences",
  "Politics": "Social Sciences",
  "Law": "Social Sciences",
  "History": "Humanities",
  "Geography": "Humanities",
  "Religious Studies": "Humanities",
  "Philosophy": "Humanities",
  "French": "Languages",
  "Spanish": "Languages",
  "German": "Languages",
  "Latin": "Languages",
  "Art and Design": "Creative & Physical",
  "Music": "Creative & Physical",
  "Drama and Theatre": "Creative & Physical",
  "Media Studies": "Creative & Physical",
  "Physical Education": "Creative & Physical",
  "Accounting": "Other",
}

# Subjects with a single rich legacy topic file already in the repo
# (topics/{slug}/{slug}.html) but not defined above with per-board content.
LEGACY_TOPIC_FILES = {
  "English Language": "language-diversity-sociolects-and-child-acquisition.html",
  "Sociology": "sociological-theories-education-and-crime.html",
  "Law": "the-english-legal-system-criminal-and-tort-law.html",
  "Politics": "uk-and-us-government-constitutions-and-ideologies.html",
  "Religious Studies": "philosophy-of-religion-ethical-theories-and-theology.html",
  "Physical Education": "biomechanics-exercise-physiology-and-sports-psychology.html",
  "Media Studies": "media-language-representation-industries-and-audiences.html",
  "French": "la-societe-francaise-immigration-et-culture.html",
  "Spanish": "sociedad-hispanica-tradiciones-y-movimientos-sociales.html",
  "German": "gesellschaft-im-wandel-und-deutsche-geschichte.html",
  "Latin": "advanced-latin-syntax-cicero-and-virgil.html",
  "Art and Design": "critical-context-material-exploration-and-creative-synthesis.html",
  "Music": "western-classical-harmony-sonata-form-and-score-analysis.html",
  "Drama and Theatre": "theatre-practitioners-devising-and-textual-interpretation.html",
  "Accounting": "financial-statements-ratio-analysis-and-costing.html",
  "Philosophy": "epistemology-moral-philosophy-and-metaphysics-of-mind.html",
}

# GENUINE per-board differences, researched from board specifications. These are
# real, verifiable differences in assessment structure, paper design and spec
# emphasis. They are applied per subject (the differences sit at subject level);
# they appear on every topic page of that subject inside a "Board differences"
# box. Keep descriptions accurate and non-fabricated; where boards genuinely
# mirror each other that is stated honestly.
BOARD_DIFFERENCES = {
  "Mathematics": {
    "AQA": "Papers split into two Pure and one Applied paper; questions are direct and "
           "structured with a traditional layout. Statistics uses a large data set. "
           "Does not test the normal approximation to the binomial distribution, "
           "and moments are examined in one dimension only.",
    "Edexcel": "Three two-hour papers (two Pure, one Applied). Predictable, formulaic "
               "papers with strong mechanics modelling. Includes the normal "
               "approximation to the binomial distribution (with continuity correction), "
               "the discrete uniform distribution and linear coding of data, and "
               "moments in two dimensions (including ladder and angled-force problems).",
    "OCR": "Follows the government core content closely. Two Pure papers plus an Applied "
           "paper. Algebra-heavy with a strong statistics emphasis on hypothesis "
           "testing; includes area between a curve and the y-axis and moments in "
           "two dimensions.",
    "WJEC": "Mainly taken in Wales. Pure plus Applied (Mechanics and Statistics) papers; "
            "content overlaps heavily with the English boards. Modular a2 assessment.",
    "CCEA": "Northern Ireland's board. Content broadly mirrors the English boards within "
            "a unitised A2 structure.",
  },
  "Further Mathematics": {
    "AQA": "Core Pure plus an optional applied component; two option papers from a "
           "pool. Good range of additional Pure content.",
    "Edexcel": "Core Pure plus two option papers chosen from Further Pure, Further "
               "Statistics, Further Mechanics and Decision Mathematics, with "
               "restrictions on combinations. The most widely taught route.",
    "OCR": "Offered as OCR A and OCR B (MEI). MEI includes a distinctive "
           "problem-solving emphasis and a comprehension-style component; strong "
           "applied element.",
    "WJEC": "Pure plus applied options; the specific pathway chosen by the centre or "
            "school determines the applied content.",
    "CCEA": "Pure-heavy specification; applied modules vary by centre.",
  },
  "Biology": {
    "AQA": "Three papers, no multiple choice, and a unique 25-mark synoptic essay in "
           "Paper 3. Twelve prescribed required practicals with specific terminology "
           "in mark schemes.",
    "Edexcel": "Three papers with multiple choice and a pre-released scientific article "
               "for Paper 3 (examined in context, apply knowledge to the article). "
               "Context-led (Salters-Nuffield style). Sixteen core practicals.",
    "OCR": "Three papers; multiple choice on Papers 1 and 2 (15 marks each). No essays, "
           "shorter extended-response throughout. Practical work organised as twelve "
           "flexible PAGs.",
    "WJEC": "Welsh board, largely unitised into five units with an externally marked "
            "practical (Unit 5). Optional topics in Unit 4 (e.g. immunology, "
            "neurobiology).",
    "CCEA": "Northern Ireland's board; unitised structure with content broadly "
            "mirroring the other boards.",
  },
  "Chemistry": {
    "AQA": "Three papers; Paper 3 includes practical-skills and synoptic multiple "
           "choice. Clear division into physical, inorganic and organic chemistry. "
           "Twelve required practicals.",
    "Edexcel": "Three papers with clear formula sheets. Sixteen core practical "
               "activities; applied and practical questions foregrounded in Paper 3.",
    "OCR": "Offered as OCR A (traditional) with a synoptic 'Unified Chemistry' Paper 3, "
           "and OCR B (Salters, context-led). Practical work runs as twelve PAGs.",
    "WJEC": "Welsh board; unitised structure. Content aligns closely with the English "
            "specifications.",
    "CCEA": "Northern Ireland's board; unitised assessment with content broadly "
            "mirroring other boards.",
  },
  "Physics": {
    "AQA": "Two written papers plus one Paper 3 covering practical skills and "
           "optional topics (e.g. astrophysics). Twelve required practicals; "
           "multiple choice on the AS papers.",
    "Edexcel": "Three papers with all topics in Papers 1 and 2 and a synoptic Paper 3. "
               "Strong emphasis on practical and data-analysis questions.",
    "OCR": "Modules 1-6; Papers 1 and 2 assess defined content and Paper 3 is "
           "unified/synoptic. Practical activities mapped to required practical "
           "criteria. Considered conceptually demanding.",
    "WJEC": "Welsh board; unitised structure with content aligning closely to the "
            "English physics specifications.",
    "CCEA": "Northern Ireland's board; unitised assessment with content broadly "
            "mirroring the other boards.",
  },
  "English Literature": {
    "AQA": "Two exam papers plus coursework; specific set texts including an "
           "anthology and both open- and closed-book components. Unseen analysis "
           "required. Both AS and A-level on the same specification.",
    "Edexcel": "Two exam papers plus a coursework option; a different set-text list. "
               "Includes poetry, prose and drama with comparative and contextual "
               "tasks.",
    "OCR": "Distinct set texts with a strong comparative element across periods; "
           "includes a non-exam assessment component.",
    "WJEC": "Welsh board with its own set-text list and unit-based exam structure.",
    "CCEA": "Northern Ireland set texts and assessment structure differ from the "
            "England boards.",
  },
  "History": {
    "AQA": "Range of British and world depth and thematic options, a source-based "
           "paper (America), plus an essay paper and a non-exam assessment.",
    "Edexcel": "Specific period studies and thematic breadth options; coursework is "
               "essential. Three externally assessed papers plus one teacher-"
               "assessed component.",
    "OCR": "Distinct units including options such as 'The Cold War', 'Russia' and "
           "'Britain'; a thematic study plus a period study with an essay-based "
           "assessment.",
    "WJEC": "Welsh-focused and British options with a unit-based assessment structure.",
    "CCEA": "Northern Ireland options with a modular assessment pattern.",
  },
  "Geography": {
    "AQA": "Physical and human papers plus a geographical skills / fieldwork "
           "component; four days of required fieldwork reported in the exam.",
    "Edexcel": "Three papers including physical, human and a synoptic paper with "
               "fieldwork examined in context.",
    "OCR": "Two examined papers plus a non-exam assessment investigating geography; "
           "strong emphasis on independent investigation.",
    "WJEC": "Welsh board; unitised structure with physical, human and skills content.",
    "CCEA": "Northern Ireland's board; unitised assessment with content broadly "
            "mirroring other boards.",
  },
  "Economics": {
    "AQA": "Three papers covering markets, the national economy and economic "
           "principles; data-response and essay-based questions.",
    "Edexcel": "Four papers with MCQ, short-answer and essay; a strong "
               "data-response component in each theme.",
    "OCR": "Two examined papers plus a non-exam assessment; emphasis on applied "
           "economics and evaluation.",
    "WJEC": "Welsh board; unitised structure covering micro and macro themes.",
    "CCEA": "Northern Ireland's board; unitised assessment with content broadly "
            "mirroring other boards.",
  },
  "Business Studies": {
    "AQA": "Three papers including one with multiple choice and resource-based "
           "questions; coursework replaced by a fully examined route.",
    "Edexcel": "Four papers with data-response and extended essays; strong emphasis "
               "on real business contexts and case-study application.",
    "OCR": "Two examined papers plus a non-exam assessment investigating a business "
           "context.",
    "WJEC": "Welsh board; unitised structure covering marketing, finance, operations "
            "and strategy.",
    "CCEA": "Northern Ireland's board; unitised assessment with content broadly "
            "mirroring other boards.",
  },
  "Computer Science": {
    "AQA": "Two papers: one on computational thinking and programming, the other "
           "theoretical. Includes a non-exam programming project.",
    "Edexcel": "Three papers plus a non-exam project; strong emphasis on "
               "Python-style programming and mathematical reasoning.",
    "OCR": "Two papers plus a substantial programming project; conceptual and "
           "theory-heavy, considered demanding.",
    "WJEC": "Welsh board; unitised structure covering programming, systems and "
            "networks.",
    "CCEA": "Northern Ireland's board; unitised assessment with content broadly "
            "mirroring other boards.",
  },
  "Psychology": {
    "AQA": "Three papers covering approaches, research methods and an issue/debates; "
           "includes questions on a compulsory research methods section.",
    "Edexcel": "Three exam papers plus a non-exam assessment (research report); "
               "foundations, applications and research methods.",
    "OCR": "Three components including a research methods paper; strong emphasis "
           "on applying psychological research.",
    "WJEC": "Welsh board; unitised structure covering approaches, methods and core "
            "areas of psychology.",
    "CCEA": "Northern Ireland's board; unitised assessment with content broadly "
            "mirroring other boards.",
  },
}


REDIRECT_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Redirecting\u2026</title>
<meta http-equiv="refresh" content="0; url={rel}">
<link rel="canonical" href="{rel}">
<script>window.location.replace("{rel}");</script>
</head><body>
<p><a href="{rel}">This page has moved. Click here to continue.</a></p>
</body></html>
"""


# Subject -> Amazon affiliate cards shown in the right-hand ad sidebar and the
# end-of-page CTA. Keyed by subject id; subjects not listed fall back to a
# generic set. Fastmail / Dynadot / Zen partner cards are always shown too.
AFFILIATES = {
  "mathematics": [
    ("Scientific Calculators", "scientific+calculator+A-Level", "Essential for A-Level Maths exams"),
    ("Graph Paper Pads", "graph+paper+a4+pad", "A4 squared paper for maths"),
    ("Maths Revision Guides", "A-Level+Maths+revision+guides", "CGP and other revision guides"),
  ],
  "further-mathematics": [
    ("Further Maths Guides", "A-Level+Further+Maths+revision", "Core Pure and option guides"),
    ("Graphic Calculators", "graphic+calculator+student", "CAS and graphing calculators"),
    ("Maths Revision Guides", "A-Level+Maths+revision+guides", "CGP and other revision guides"),
  ],
  "biology": [
    ("Biology Revision Guides", "A-Level+Biology+revision+guides", "CGP, Oxford, and more"),
    ("Microscope Slides", "microscope+slides+prepared", "Prepared slides for practicals"),
    ("Biology Field Guides", "A-Level+biology+fieldwork+guide", "Required practical support"),
  ],
  "chemistry": [
    ("Chemistry Revision Guides", "A-Level+Chemistry+revision+guides", "CGP, Oxford, and more"),
    ("Molecular Model Kits", "molecular+model+kit+organic", "Visualise chemical structures"),
    ("Periodic Table Posters", "periodic+table+poster+large", "Wall reference for chemistry"),
  ],
  "physics": [
    ("Physics Revision Guides", "A-Level+Physics+revision+guides", "CGP, Oxford, and more"),
    ("Data Loggers", "data+logger+physics+education", "For required practicals"),
    ("Multimeters", "digital+multimeter+student", "Essential for electricity practicals"),
  ],
  "english-literature": [
    ("Literature Study Guides", "A-Level+English+Literature+guides", "York Notes, CGP, and more"),
    ("Set Text Collections", "A-Level+English+Literature+set+texts", "Complete play/novel editions"),
    ("Annotation Sticky Notes", "sticky+notes+annotation", "For text analysis"),
  ],
  "english-language": [
    ("English Language Guides", "A-Level+English+Language+revision", "CGP, York Notes, and more"),
    ("Set Text Editions", "A-Level+English+set+texts", "Annotated editions for study"),
    ("Highlighters & Pens", "highlighter+pens+study", "For text annotation"),
  ],
  "history": [
    ("History Revision Guides", "A-Level+History+revision+guides", "Topic-specific guides"),
    ("Timeline Wall Charts", "history+timeline+poster", "Visual reference for chronology"),
    ("Source Analysis Workbooks", "A-Level+history+source+analysis", "Practice source questions"),
  ],
  "geography": [
    ("Geography Revision Guides", "A-Level+Geography+revision+guides", "CGP, Oxford, and more"),
    ("Atlas", "world+atlas+student", "Essential for map skills"),
    ("Case Study Flashcards", "A-Level+geography+case+study+cards", "Key facts for case studies"),
  ],
  "economics": [
    ("Economics Revision Guides", "A-Level+Economics+revision+guides", "Micro and macro"),
    ("Economics Textbooks", "A-Level+Economics+textbook", "Core textbooks"),
    ("Graph Paper", "economics+graph+paper+a4", "For diagrams"),
  ],
  "psychology": [
    ("Psychology Revision Guides", "A-Level+Psychology+revision+guides", "Studies, theories, methods"),
    ("Research Methods Workbooks", "psychology+research+methods+A-Level", "Experiments, ethics"),
    ("Study Cards", "psychology+flashcards+A-Level", "Key studies and theories"),
  ],
  "business-studies": [
    ("Business Revision Guides", "A-Level+Business+revision+guides", "CGP, Tutor2u, and more"),
    ("Case Study Books", "A-Level+business+case+studies", "Real business examples"),
    ("Financial Calculators", "financial+calculator+student", "For finance topics"),
  ],
  "computer-science": [
    ("CS Revision Guides", "A-Level+Computer+Science+revision", "CGP, PG Online, and more"),
    ("Python Books", "python+programming+A-Level", "Beginner to advanced Python"),
    ("Raspberry Pi Kits", "raspberry+pi+starter+kit", "For programming projects"),
  ],
  "sociology": [
    ("Sociology Revision Guides", "A-Level+Sociology+revision+guides", "Families, education, crime"),
    ("Sociology Textbooks", "A-Level+Sociology+textbook", "Core concepts and theorists"),
    ("Essay Planning Pads", "essay+planning+pad+a4", "Structure long answers"),
  ],
}

DEFAULT_AFFILIATES = [
  ("A-Level Revision Guides", "A-Level+revision+guides", "All subjects covered"),
  ("Study Stationery", "study+stationery+student", "Pens, highlighters, flashcards"),
  ("Revision Timetable", "revision+timetable+planner", "Plan your study schedule"),
]


def affiliate_cards(subject_id):
    """Amazon affiliate + partner cards for the right-hand ad sidebar."""
    affs = AFFILIATES.get(subject_id, DEFAULT_AFFILIATES)
    cards = []
    for title, search, desc in affs[:3]:
        cards.append(
            '<a href="https://www.amazon.co.uk/s?k={}&tag=scottrix-21" class="affiliate-card" target="_blank" rel="nofollow noopener">\n'
            '<div class="affiliate-card-title">{}</div>\n'
            '<div class="affiliate-card-desc">{}</div>\n'
            '<div class="affiliate-card-store"><img src="../../amazon-smile.svg" alt="Amazon"> amazon.co.uk</div>\n'
            '</a>'.format(search, title, desc)
        )
    cards += [
        '<a href="https://join.fastmail.com/0d63b2d52105" class="affiliate-card" target="_blank" rel="nofollow noopener">'
        '<div class="affiliate-card-title">Fastmail — Private Email</div>'
        '<div class="affiliate-card-desc">Privacy-first email with no ads and no tracking</div>'
        '<div class="affiliate-card-store">fastmail.com</div></a>',
        '<a href="https://www.dynadot.com/?ref=scottrix" class="affiliate-card" target="_blank" rel="nofollow noopener">'
        '<div class="affiliate-card-title">Dynadot — Domain Registration →</div>'
        '<div class="affiliate-card-desc">Register or transfer domains with free SSL and affordable pricing</div>'
        '<div class="affiliate-card-store">dynadot.com</div></a>',
        '<a href="https://zen.mention-me.com/m/ol/yv3qsjix-scott-harrison" class="affiliate-card" target="_blank" rel="nofollow noopener">'
        '<div class="affiliate-card-title">Zen Internet — UK Broadband →</div>'
        '<div class="affiliate-card-desc">Award-winning UK broadband with no data caps and great customer service</div>'
        '<div class="affiliate-card-store">zen.co.uk</div></a>',
    ]
    return "\n".join(cards)


def topic_page(subject_name, topic, site, mode, board_diffs):
    """Build one collapsed, board-agnostic topic page in the full site layout
    (header, breadcrumb, ad banners, sectioned content, ad-right sidebar,
    footer) matching the gcserevise topic-page format."""
    esc = html.escape
    title = topic["title"]
    sslug = slug(subject_name)
    tslug = slug(title)
    subject_id = sslug
    domain = f"https://scottrix.github.io/{site}"
    page_url = f"{domain}/topics/{sslug}/{tslug}.html"
    subject_label = f"{subject_name}"
    link_root = "../../"

    # Board differences
    diffs = board_diffs.get(subject_name, {})
    diffs_html = ""
    if diffs:
        rows = "".join(
            f'<div class="key-point"><strong>{esc(b)}:</strong> {esc(n)}</div>'
            for b, n in diffs.items()
        )
        diffs_html = f"""<section class="section">
<h2>🔀 Board Differences</h2>
<p>Board specifications differ in assessment structure and emphasis. The core content below is shared across boards; these are the genuine differences by board:</p>
{rows}
</section>"""

    # Content sections
    objectives = "".join(f"<li>{esc(o)}</li>" for o in topic["objectives"])
    keypts = "".join(
        f'<div class="key-point"><strong>Key Fact:</strong> {esc(k)}</div>'
        for k in topic["key"]
    )
    practice_items = "".join(f"<li>{esc(p)}</li>" for p in topic["practice"])

    objectives_section = ""
    if objectives:
        objectives_section = f"""<section class="section">
<h2>🎯 Learning Objectives</h2>
<ul>{objectives}</ul>
</section>"""

    keypoints_section = f"""<section class="section">
<h2>📌 Key Points</h2>
{keypts}
</section>"""

    example_section = f"""<section class="section">
<h2>💡 Worked Example</h2>
<div class="example">
<div class="example-title">Exam-Style Question</div>
<p><strong>Question:</strong> {esc(topic['example'])}</p>
<div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid var(--border);">
<p><strong>Model Answer:</strong></p>
<p>{esc(topic['answer'])}</p>
</div>
</div>
</section>"""

    practice_section = ""
    if practice_items:
        practice_section = f"""<section class="section">
<h2>❓ Practice Questions</h2>
<div class="practice-questions">
<div class="question">
<p><strong>Questions:</strong></p>
<ul>{practice_items}</ul>
</div>
</div>
</section>"""

    if mode == "Lessons":
        lesson_section = f"""<section class="section">
<h2>📚 Lesson Plan (50 minutes)</h2>
<ol>
<li><strong>Starter (5 min):</strong> Recall prior knowledge of {esc(title.lower())} with quick questions.</li>
<li><strong>Teaching (15 min):</strong> Work through each of the learning objectives, explaining principles step by step.</li>
<li><strong>Key points review (5 min):</strong> Revisit the key points together, confirming understanding.</li>
<li><strong>Worked example (10 min):</strong> Model the example question: {esc(topic['example'])}. Solution: {esc(topic['answer'])}</li>
<li><strong>Practice (10 min):</strong> Students attempt the practice questions independently; circulate and support.</li>
<li><strong>Plenary (5 min):</strong> Review answers and address misconceptions.</li>
</ol>
</section>
<section class="section">
<h2>🏠 Homework</h2>
<ul>{practice_items}</ul>
</section>
<section class="section">
<h2>🧾 Assessment</h2>
<p>Check practice answers against the model answer; use the built-in practice questions as formative assessment.</p>
</section>"""
    else:
        lesson_section = ""

    meta_desc = (f"A-Level {esc(subject_name)} revision: {esc(title)}. "
                 f"Learning objectives, key points, worked examples and practice questions across AQA, Edexcel, OCR, WJEC and CCEA.")
    twitter_desc = f"{esc(title)} — A-Level {esc(subject_name)} revision notes."

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<script>/* gcanonical-redirect */(function(){{var p=location.pathname,q=location.search,h=location.hash,m=/^(.*)\\/index\\.html$/.exec(p);if(m){{location.replace(m[1]+"/"+q+h);return}}if(!p.endsWith("/")&&!/\\.[a-z0-9]{{1,10}}$/i.test(p)){{location.replace(p+".html"+q+h)}}}})();</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} - A-Level {esc(subject_name)} {mode} Notes</title>
<meta name="description" content="{meta_desc}">
<meta name="keywords" content="A-Level {esc(subject_name)}, {esc(title)}, revision notes, past papers, AQA, Edexcel, OCR, WJEC, CCEA">
<meta property="og:title" content="{esc(title)} - A-Level {esc(subject_name)}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{page_url}">
<link rel="canonical" href="{page_url}">
<meta property="og:site_name" content="A-Level {mode}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{twitter_desc}">
<link rel="stylesheet" href="{link_root}style.css">
</head>
<body>
<header class="site-header">
<div class="header-content">
<a href="{link_root}index.html" class="logo">📚 A-Level {mode}</a>
<nav class="nav">
<a href="{link_root}index.html#subjects">Subjects</a>
<a href="{link_root}{sslug}.html">{esc(subject_name)}</a>
</nav>
<button id="theme-toggle" class="theme-btn">🌙</button>
</div>
</header>

<main class="topic-content">
<div class="disclaimer-banner"><strong>A-Level {mode} Aid:</strong> This resource is designed to support your revision and may contain errors. If you find a discrepancy with your class teaching, your teacher is correct — please let us know at <a href="mailto:alevelrevise@scott.scottrix.co.uk">alevelrevise@scott.scottrix.co.uk</a>.</div>

<nav class="breadcrumb">
<a href="{link_root}index.html">Home</a> <span>›</span>
<a href="{link_root}{sslug}.html">{esc(subject_name)}</a> <span>›</span>
<span>{esc(title)}</span>
</nav>

<article class="topic-header">
<h1>{esc(title)}</h1>
<div class="topic-meta">
<span class="badge foundation">Year 1 / AS</span><span class="badge higher">Year 2 / A-Level</span>
<span class="badge">All Boards (AQA, Edexcel, OCR, WJEC, CCEA)</span>
</div>
<p class="topic-desc">{meta_desc}</p>
</article>

<a class="fastmail-topbar" data-banner="fastmail" href="https://join.fastmail.com/0d63b2d52105" target="_blank" rel="noopener"><img src="{link_root}FM Billboard 970x250.png" alt="Fastmail" loading="lazy"></a>
<a class="fastmail-topbar" data-banner="dynadot" href="https://www.dynadot.com/?ref=scottrix" target="_blank" rel="nofollow noopener" hidden><img src="{link_root}dynadot-banner.jpg" alt="Dynadot — register a new domain, web hosting, SSL" loading="lazy" onerror="this.parentElement.style.display='none';document.querySelector('[data-banner=fastmail]').hidden=false"></a>
<script>(function(){{var fm=document.querySelector('[data-banner=fastmail]');var dd=document.querySelector('[data-banner=dynadot]');if(Math.random()<0.5){{fm.hidden=true;dd.hidden=false}}}})();</script>

{keypoints_section}
{objectives_section}
{diffs_html}
{example_section}
{practice_section}
{lesson_section}

<nav class="topic-nav">
<a href="{link_root}{sslug}.html">← Back to {esc(subject_name)} Overview</a>
<a href="{link_root}index.html">All Subjects →</a>
</nav>
</main>
<footer class="site-footer">
<p>A-Level {mode} - Free revision notes for all subjects and exam boards</p>
<p>Content for educational purposes only. Always cross-reference with official specifications.</p>
<p>This site contains affiliate links. We may earn a commission if you purchase through these links.</p>
<p>© 2025 | <a href="https://github.com/scottrix/{site}">GitHub</a> | <a href="{link_root}privacy.html">Privacy Policy</a> | <a href="mailto:alevelrevise@scott.scottrix.co.uk">Contact</a></p>
</footer>
<script>
document.getElementById('theme-toggle').addEventListener('click', function() {{
const root = document.documentElement;
if (root.classList.contains('light-mode')) {{
root.classList.remove('light-mode'); this.textContent = '🌙'; localStorage.setItem('{site}-theme', 'dark');
}} else {{
root.classList.add('light-mode'); this.textContent = '☀️'; localStorage.setItem('{site}-theme', 'light');
}}
}});
if (localStorage.getItem('{site}-theme') === 'light') {{
document.documentElement.classList.add('light-mode'); document.getElementById('theme-toggle').textContent = '☀️';
}}
</script>
<aside class="ad-right">
{affiliate_cards(subject_id)}
</aside>
<script src="{link_root}sidebar.js"></script>
<script src="{link_root}affiliate-images.js"></script>
</body></html>"""
    return page


def build():
    for site, mode in (("alevelrevise", "Revise"), ("alevellessons", "Lessons")):
        base = os.path.join(ROOT, site)
        os.makedirs(base, exist_ok=True)
        output = {"subjects": []}
        seen = set()
        for subject in SUBJECTS:
            subj_entry = {
                "name": subject["name"],
                "id": slug(subject["name"]),
                "category": CATEGORIES.get(subject["name"], "Core"),
                "boards": list(BOARDS),
                "topics": [],
            }
            subj_dir = os.path.join(base, "topics", slug(subject["name"]))
            os.makedirs(subj_dir, exist_ok=True)
            written_slugs = set()
            for topic in subject["topics"]:
                tslug = slug(topic["title"])
                written_slugs.add(tslug)
                page = f"topics/{slug(subject['name'])}/{tslug}.html"
                subj_entry["topics"].append({
                    "title": topic["title"],
                    "learningObjectives": topic["objectives"],
                    "keyPoints": topic["key"],
                    "exampleQuestion": topic["example"],
                    "modelAnswer": topic["answer"],
                    "practiceQuestions": topic["practice"],
                    "page": page,
                })
                content = topic_page(subject["name"], topic, site, mode, BOARD_DIFFERENCES)
                with open(os.path.join(subj_dir, f"{tslug}.html"), "w") as f:
                    f.write(content)
                # Collapse old per-board pages: replace them with 301-style
                # redirects to the single collapsed topic page.
                for board in BOARDS:
                    board_dir = os.path.join(subj_dir, slug(board))
                    old_path = os.path.join(board_dir, f"{tslug}.html")
                    if os.path.isdir(board_dir):
                        os.makedirs(board_dir, exist_ok=True)
                        rel = f"../{tslug}.html"
                        with open(old_path, "w") as f:
                            f.write(REDIRECT_TEMPLATE.format(rel=rel))
            # Wire in any rich legacy flat topic files sitting in the subject dir
            # that were NOT written as collapsed pages by this generator.
            flat = flat_general_board(base, subject["name"], mode, written_slugs)
            if flat:
                subj_entry["topics"].extend(flat)
            output["subjects"].append(subj_entry)
            seen.add(subject["name"])

        # Add the 16 legacy subjects that already have a rich flat topic file,
        # so subjects.json covers all 28. Preserve existing topic files (do not
        # overwrite them); only their subjects.json entry is (re)built.
        for name, top_file in LEGACY_TOPIC_FILES.items():
            if name in seen:
                continue
            subj = slug(name)
            path = os.path.join(base, "topics", subj, slug(top_file))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            topics = []
            if os.path.exists(path):
                topics.append({
                    "title": name,
                    "learningObjectives": [],
                    "keyPoints": [],
                    "exampleQuestion": "",
                    "modelAnswer": "",
                    "practiceQuestions": [],
                    "page": f"topics/{subj}/{slug(top_file)}",
                })
            output["subjects"].append({
                "name": name,
                "boards": ["General"],
                "id": subj,
                "category": CATEGORIES.get(name, "Core"),
                "topics": topics,
            })
            seen.add(name)

        # Sort subjects by the index order used on the home page.
        order = ["Mathematics", "Further Mathematics", "English Literature", "English Language",
                 "Biology", "Chemistry", "Physics", "Computer Science",
                 "Economics", "Psychology", "Sociology", "Business Studies", "Politics", "Law",
                 "History", "Geography", "Religious Studies", "Philosophy",
                 "French", "Spanish", "German", "Latin",
                 "Art and Design", "Music", "Drama and Theatre", "Media Studies", "Physical Education",
                 "Accounting"]
        name_to_subj = {s["name"]: s for s in output["subjects"]}
        output["subjects"] = [name_to_subj[n] for n in order if n in name_to_subj]

        with open(os.path.join(base, "subjects.json"), "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"built {site}: {len(output['subjects'])} subjects (collapsed single-topic pages)")

if __name__ == "__main__":
    build()
