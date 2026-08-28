"""Generate A-Level revision and lesson content for scottrix.github.io."""
import json, os, html

ROOT = '/home/scott/src/scottrix.github.io'
BOARDS = ["AQA", "Edexcel", "OCR", "WJEC", "CCEA"]

# Each subject: name + topics. Each topic: title, objectives[], key[], example,
# answer, practice[], and optional boardNotes (dict board->note appended to key points).
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

# Per-board notes where specs genuinely differ; generic otherwise.
BOARD_NOTES = {
  "Mathematics": {
    "AQA": "Spec taught as Pure, Mechanics, and Statistics papers.",
    "Edexcel": "Papers split into Pure Mathematics and Applied (Mechanics + Statistics).",
    "OCR": "Two Pure papers plus one Applied (Mechanics or Statistics options).",
    "WJEC": "Similar Pure/Applied split; pure content overlaps heavily with AQA/Edexcel.",
    "CCEA": "Northern Ireland board; content broadly mirrors the other boards.",
  },
  "Further Mathematics": {
    "AQA": "Includes additional Pure plus an optional decision/applied module.",
    "Edexcel": "Additional Pure plus two applied options (e.g. Further Mechanics, Decision).",
    "OCR": "Frequently paired with the 'MEI' specification; strong applied component.",
    "WJEC": "Pure plus applied options; check the specific pathway chosen.",
    "CCEA": "Pure-heavy; applied modules vary by centre.",
  },
  "English Literature": {
    "AQA": "Set texts include specific novels, plays and an anthology; unseen analysis required.",
    "Edexcel": "Different set list of texts; includes poetry, prose and drama plus coursework.",
    "OCR": "Distinct set texts and a strong comparative element across periods.",
    "WJEC": "Welsh exam board with its own set-text list and exam structure.",
    "CCEA": "Northern Ireland set texts and assessment differ from England boards.",
  },
  "History": {
    "AQA": "Range of British and world depth/thematic options; source-based paper.",
    "Edexcel": "Specific period studies and thematic breadth options; coursework essential.",
    "OCR": "Distinct units including 'The Cold War', 'Russia' and 'Britain' options.",
    "WJEC": "Welsh-focused and British options; unit-based assessment.",
    "CCEA": "Northern Ireland options and modular assessment.",
  },
}
DEFAULT_NOTE = {
  "AQA": "AQA specification; content aligns with the national A-Level syllabus.",
  "Edexcel": "Edexcel (Pearson) specification; check the specific content list for your paper.",
  "OCR": "OCR specification; note any options relevant to your centre.",
  "WJEC": "WJEC specification; mainly taken in Wales.",
  "CCEA": "CCEA specification; taken in Northern Ireland.",
}

def tile(topic_title, subject, board, topic, mode, note):
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{topic_title} - {subject} ({board})</title><link rel="stylesheet" href="../../style.css">
</head><body>
<header class="site-header"><div class="header-inner">
<a href="../../index.html" class="logo">📚 A-Level {mode}</a></div></header>
<main><section class="site-section">
<h1>{subject} — {topic['title']}</h1>
<p><strong>Exam board:</strong> {board} &nbsp;|&nbsp; <a href="../../index.html">Back to subjects</a></p>
<h2>Board-Specific Note</h2><p>{note}</p>
<h2>Learning Objectives</h2><ul>{''.join(f'<li>{o}</li>' for o in topic['objectives'])}</ul>
<h2>Key Points</h2><ul>{''.join(f'<li>{k}</li>' for k in topic['key'])}</ul>"""

def revise_page(subject, board, topic, note):
    t = tile(topic['title'], subject['name'], board, topic, "Revise", note)
    t += f"""<h2>Example Question</h2><p>{topic['example']}</p>
<h2>Model Answer</h2><p>{topic['answer']}</p>
<h2>Practice Questions</h2><ul>{''.join(f'<li>{p}</li>' for p in topic['practice'])}</ul>
</section></main></body></html>"""
    return t

def lesson_page(subject, board, topic, note):
    t = tile(topic['title'], subject['name'], board, topic, "Lessons", note)
    t += f"""<h2>Lesson Plan (50 minutes)</h2>
<ol><li><strong>Starter (5 min):</strong> Recall prior knowledge of {topic['title'].lower()} with quick questions.</li>
<li><strong>Teaching (15 min):</strong> Work through each of the learning objectives, explaining principles step by step.</li>
<li><strong>Key points review (5 min):</strong> Revisit the key points together, confirming understanding.</li>
<li><strong>Worked example (10 min):</strong> Model the example question: {topic['example']}. Solution: {topic['answer']}</li>
<li><strong>Practice (10 min):</strong> Students attempt the practice questions independently; circulate and support.</li>
<li><strong>Plenary (5 min):</strong> Review answers and address misconceptions.</li></ol>
<h2>Homework</h2><ul>{''.join(f'<li>{p}</li>' for p in topic['practice'])}</ul>
<h2>Assessment</h2><p>Check practice answers against the model answer; use the built-in practice questions as formative assessment.</p>
</section></main></body></html>"""
    return t

def build():
    for site, mode in (("alevelrevise", "Revise"), ("alevellessons", "Lessons")):
        base = os.path.join(ROOT, site)
        os.makedirs(base, exist_ok=True)
        output = {"subjects": []}
        for subject in SUBJECTS:
            subj_entry = {"name": subject["name"], "boards": []}
            notes = BOARD_NOTES.get(subject["name"], DEFAULT_NOTE)
            for board in BOARDS:
                board_entry = {"board": board, "topics": []}
                note = notes.get(board, DEFAULT_NOTE[board])
                tdir = os.path.join(base, slug(subject["name"]), slug(board))
                os.makedirs(tdir, exist_ok=True)
                for topic in subject["topics"]:
                    tslug = slug(topic["title"])
                    jtopic = {
                        "title": topic["title"],
                        "boardNote": note,
                        "learningObjectives": topic["objectives"],
                        "keyPoints": topic["key"],
                        "exampleQuestion": topic["example"],
                        "modelAnswer": topic["answer"],
                        "practiceQuestions": topic["practice"],
                        "page": f"{slug(subject['name'])}/{slug(board)}/{tslug}.html",
                    }
                    board_entry["topics"].append(jtopic)
                    content = (lesson_page if mode == "Lessons" else revise_page)(subject, board, topic, note)
                    with open(os.path.join(tdir, f"{tslug}.html"), "w") as f:
                        f.write(content)
                subj_entry["boards"].append(board_entry)
            output["subjects"].append(subj_entry)
        with open(os.path.join(base, "subjects.json"), "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"built {site}: {len(output['subjects'])} subjects")

if __name__ == "__main__":
    build()
