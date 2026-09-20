#!/usr/bin/env python3
"""
Comprehensive Curriculum Data & Builder for all 28 A-Level Subjects.
"""

import os
import json
import re
from pathlib import Path

BASE = Path('/home/scott/src/scottrix.github.io')

# Helper to build standard topic
def make_topic(tid, title, slug, desc, defs, key_pts, ex_q, ex_a, practice=None):
    if practice is None:
        practice = [
            (f"Explain the significance of {title} in A-Level examination contexts.", f"Demonstrate clear conceptual understanding of {title}, defining core terminology and citing relevant principles or case examples."),
            (f"Evaluate key arguments or methodologies concerning {title}.", f"Contrast competing perspectives, discuss empirical evidence or theoretical limitations, and synthesize a balanced, well-reasoned conclusion.")
        ]
    return {
        "id": tid,
        "title": title,
        "slug": slug,
        "desc": desc,
        "definitions": [{"term": t, "def": d} for t, d in defs],
        "key_points": key_pts,
        "example": {"q": ex_q, "a": ex_a},
        "practice": [{"q": q, "a": a} for q, a in practice]
    }

# 28 Full Curriculum Subjects
CURRICULUM = [
    # 1. Mathematics
    {
        "name": "Mathematics",
        "slug": "mathematics",
        "category": "Core",
        "strands": [
            {
                "strand": "Pure Mathematics",
                "topics": [
                    make_topic(
                        "M1", "Algebraic Methods and Proof", "algebraic-methods-and-proof",
                        "Proof by deduction, contradiction, exhaustion; algebraic fractions and partial fractions.",
                        [
                            ("Proof by Contradiction", "Establishing truth by demonstrating that assuming the statement to be false leads to a logical contradiction."),
                            ("Partial Fractions", "Decomposing rational fractions P(x)/Q(x) into sums of simpler terms with linear or quadratic denominators.")
                        ],
                        [
                            "To prove √2 is irrational, assume √2 = a/b in lowest terms, square to get 2b² = a², deduce a and b are both even, contradicting lowest terms.",
                            "Partial fraction forms: A/(ax+b) + B/(cx+d) for distinct linear factors; A/(ax+b) + B/(ax+b)² for repeated factors.",
                            "Improper fractions (deg numerator ≥ deg denominator) must first be divided by polynomial division."
                        ],
                        "Express (5x - 2) / ((x - 2)(x + 1)) in partial fractions.",
                        "Set 5x - 2 = A(x + 1) + B(x - 2).\nx = 2: 8 = 3A => A = 8/3.\nx = -1: -7 = -3B => B = 7/3.\nResult: 8/(3(x - 2)) + 7/(3(x + 1)).",
                        [
                            ("Prove by contradiction that there are infinitely many primes.", "Assume finitely many primes p₁..pₙ. Let N = p₁p₂..pₙ + 1. N is prime or has a prime factor not in the list, contradicting finiteness."),
                            ("Express (3x² + 7x - 2) / ((x - 1)(x + 2)²) in partial fractions.", "A/(x-1) + B/(x+2) + C/(x+2)². A = 8/9, B = 19/9, C = -4/3.")
                        ]
                    ),
                    make_topic(
                        "M2", "Coordinate Geometry and Circles", "coordinate-geometry-and-circles",
                        "Equations of circles, tangents and normals, intersection of lines and circles.",
                        [
                            ("Circle Equation", "(x - a)² + (y - b)² = r² with centre (a, b) and radius r."),
                            ("Tangent", "A straight line perpendicular to the radius at the point of contact.")
                        ],
                        [
                            "General circle form: x² + y² + 2gx + 2fy + c = 0 has centre (-g, -f) and radius √(g² + f² - c).",
                            "Gradient of normal at (x₁, y₁) is (y₁ - b)/(x₁ - a); gradient of tangent is perpendicular negative reciprocal.",
                            "To find intersections with line y = mx + c, substitute into circle equation and test discriminant Δ."
                        ],
                        "Find the equation of the tangent to (x - 3)² + (y + 2)² = 25 at (7, 1).",
                        "Centre (3, -2). m_radius = (1 - (-2))/(7 - 3) = 3/4.\nm_tangent = -4/3.\nEquation: y - 1 = -4/3(x - 7) => 4x + 3y - 31 = 0.",
                        [
                            ("Find the centre and radius of x² + y² - 6x + 8y - 11 = 0.", "(x - 3)² + (y + 4)² = 36. Centre (3, -4), radius = 6."),
                            ("Determine intersections of y = 2x + 5 with x² + y² = 5.", "x² + (2x + 5)² = 5 => 5x² + 20x + 20 = 0 => (x + 2)² = 0. Tangent at (-2, 1).")
                        ]
                    ),
                    make_topic(
                        "M3", "Calculus: Differentiation and Integration", "calculus-differentiation-and-integration",
                        "Chain, product, quotient rules, implicit/parametric differentiation, integration by parts and substitution.",
                        [
                            ("Product Rule", "d/dx[uv] = u(dv/dx) + v(du/dx)."),
                            ("Integration by Parts", "∫ u (dv/dx) dx = uv - ∫ v (du/dx) dx.")
                        ],
                        [
                            "Standard derivatives: d/dx[e^{kx}] = k e^{kx}, d/dx[ln x] = 1/x, d/dx[tan kx] = k sec² kx.",
                            "Parametric: dy/dx = (dy/dt) / (dx/dt); d²y/dx² = [d/dt(dy/dx)] / (dx/dt).",
                            "Separable differential equations: ∫ (1/g(y)) dy = ∫ f(x) dx + C."
                        ],
                        "Evaluate ∫₀¹ x e²ˣ dx using integration by parts.",
                        "u = x => du = dx; dv = e²ˣ dx => v = ½e²ˣ.\n[½x e²ˣ]₀¹ - ∫₀¹ ½e²ˣ dx = ½e² - [¼e²ˣ]₀¹ = ¼e² + ¼.",
                        [
                            ("Differentiate y = (x² + 1) e³ˣ.", "dy/dx = 2x e³ˣ + 3(x² + 1) e³ˣ = e³ˣ(3x² + 2x + 3)."),
                            ("Solve dy/dx = 2xy with y(0) = 3.", "∫ (1/y) dy = ∫ 2x dx => ln y = x² + C => y = 3e^{x²}.")
                        ]
                    )
                ]
            },
            {
                "strand": "Statistics and Mechanics",
                "topics": [
                    make_topic(
                        "M4", "Statistical Distributions and Hypothesis Testing", "statistical-distributions-and-hypothesis-testing",
                        "Binomial and Normal distributions, central limit theorem, one- and two-tailed hypothesis tests.",
                        [
                            ("Binomial Distribution", "X ~ B(n, p) for n independent trials with constant success probability p."),
                            ("Normal Distribution", "X ~ N(μ, σ²) continuous symmetric distribution standardised via Z = (X - μ)/σ.")
                        ],
                        [
                            "Binomial P(X = r) = ⁿCᵣ pʳ (1-p)ⁿ⁻ʳ.",
                            "Reject H₀ if test statistic falls within critical region or p-value < significance level α.",
                            "Normal distribution 68-95-99.7 rule: ~68.3% within 1σ, ~95.4% within 2σ, ~99.7% within 3σ."
                        ],
                        "A fair coin is tossed 20 times. 15 heads are observed. Test at 5% level if the coin is biased.",
                        "H₀: p = 0.5, H₁: p ≠ 0.5 (two-tailed, α = 0.025 per tail).\nX ~ B(20, 0.5). P(X ≥ 15) = 1 - P(X ≤ 14) = 0.0207.\n0.0207 < 0.025 => Reject H₀; significant evidence of bias.",
                        [
                            ("If X ~ N(100, 15²), find P(85 < X < 115).", "Z = ±1. P(-1 < Z < 1) = 0.8413 - 0.1587 = 0.6826 (68.3%)."),
                            ("State conditions for binomial modeling.", "Fixed number of trials n, two outcomes, constant probability p, independent trials.")
                        ]
                    ),
                    make_topic(
                        "M5", "Mechanics: Dynamics and Kinematics", "mechanics-dynamics-and-kinematics",
                        "SUVAT equations, variable acceleration calculus, Newton's laws, friction, connected particles, projectiles.",
                        [
                            ("Newton's 2nd Law", "Resultant Force ΣF = ma (in Newtons)."),
                            ("Friction", "F_max = μR where μ is coefficient of friction and R is normal reaction.")
                        ],
                        [
                            "Calculus kinematics: r(t) → differentiate → v(t) → differentiate → a(t).",
                            "Projectiles: a_x = 0 (constant horizontal velocity u cos θ); a_y = -9.8 m/s².",
                            "Connected particles: formulate F = ma equation for each mass, solve simultaneously."
                        ],
                        "Mass 4 kg on a 30° rough slope with μ = 0.2. Find acceleration down slope.",
                        "R = mg cos 30° = 4(9.8)(√3/2) = 33.95 N.\nFriction = 0.2 × 33.95 = 6.79 N.\nWeight down slope = 4(9.8) sin 30° = 19.6 N.\nΣF = 19.6 - 6.79 = 12.81 N => a = 12.81 / 4 = 3.20 m/s².",
                        [
                            ("Velocity v(t) = 3t² - 12t + 9. Find displacement from t=0 to 3.", "s(t) = t³ - 6t² + 9t. s(3) = 27 - 54 + 27 = 0 m."),
                            ("Connected masses 3 kg and 5 kg over a pulley. Find acceleration.", "5g - T = 5a, T - 3g = 3a => 2g = 8a => a = 2.45 m/s².")
                        ]
                    )
                ]
            }
        ]
    },

    # 2. Further Mathematics
    {
        "name": "Further Mathematics",
        "slug": "further-mathematics",
        "category": "Core",
        "strands": [
            {
                "strand": "Further Pure Mathematics",
                "topics": [
                    make_topic(
                        "FM1", "Complex Numbers and De Moivre's Theorem", "complex-numbers-and-de-moivres-theorem",
                        "Modulus-argument form, De Moivre's Theorem, roots of unity, loci in the complex plane.",
                        [
                            ("De Moivre's Theorem", "[r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ) for all n ∈ ℤ."),
                            ("Roots of Unity", "Solutions to zⁿ = 1: z_k = e^{i 2kπ/n} for k = 0, 1, ..., n-1.")
                        ],
                        [
                            "Euler's formula: e^{iθ} = cos θ + i sin θ; e^{iπ} + 1 = 0.",
                            "Loci: |z - z₁| = r is a circle centre z₁; |z - z₁| = |z - z₂| is perpendicular bisector.",
                            "Non-real roots of real polynomials occur in complex conjugate pairs z and z̄."
                        ],
                        "Express cos 3θ in terms of cos θ using De Moivre's Theorem.",
                        "(cos θ + i sin θ)³ = cos³θ + 3i cos²θ sin θ - 3 cos θ sin²θ - i sin³θ.\nReal part: cos 3θ = cos³θ - 3 cos θ (1 - cos²θ) = 4 cos³θ - 3 cos θ.",
                        [
                            ("Find all solutions to z⁴ = -16.", "z = 2 e^{i(π/4 + kπ/2)} => √2(±1 ± i)."),
                            ("Describe the locus |z - 3i| = 2.", "A circle with centre (0, 3) and radius 2.")
                        ]
                    ),
                    make_topic(
                        "FM2", "Matrices and Linear Transformations", "matrices-and-linear-transformations",
                        "2D/3D matrix transformations, determinants, inverses, eigenvalues, eigenvectors, systems of equations.",
                        [
                            ("Determinant", "Scalar scale factor for area/volume. det(A) = ad - bc for 2x2."),
                            ("Eigenvector", "Non-zero vector v satisfying Av = λv for eigenvalue λ.")
                        ],
                        [
                            "Rotation by θ: [[cos θ, -sin θ], [sin θ, cos θ]]. Reflection in y = x tan θ: [[cos 2θ, sin 2θ], [sin 2θ, -cos 2θ]].",
                            "System of 3 planes Ax = b: unique solution if det A ≠ 0; inconsistent (prism) or line of solutions (sheaf) if det A = 0.",
                            "Diagonalisation: A = PDP⁻¹ where D is diagonal eigenvalue matrix and P is eigenvector matrix."
                        ],
                        "Find eigenvalues of A = [[4, 1], [2, 3]].",
                        "det(A - λI) = (4 - λ)(3 - λ) - 2 = λ² - 7λ + 10 = (λ - 2)(λ - 5) = 0.\nEigenvalues: λ₁ = 2, λ₂ = 5.",
                        [
                            ("Find inverse of [[1, 2], [3, 4]].", "det = -2. Inverse = -½ [[4, -2], [-3, 1]] = [[-2, 1], [1.5, -0.5]]."),
                            ("Explain geometric meaning of det(M) = -1.", "Area scale factor is 1, but orientation is reversed (reflection).")
                        ]
                    )
                ]
            }
        ]
    },

    # 3. Biology
    {
        "name": "Biology",
        "slug": "biology",
        "category": "Sciences",
        "strands": [
            {
                "strand": "Biological Molecules and Cell Biology",
                "topics": [
                    make_topic(
                        "B1", "Biological Molecules and Enzyme Kinetics", "biological-molecules-and-enzyme-kinetics",
                        "Carbohydrates, lipids, proteins, nucleic acids, ATP, enzyme kinetics, competitive and non-competitive inhibition.",
                        [
                            ("Induced Fit Model", "Substrate binding causes conformational change in enzyme's active site, lowering activation energy."),
                            ("Primary Structure", "Unique sequence of amino acids linked by covalent peptide bonds in a polypeptide.")
                        ],
                        [
                            "Condensation joins monomers releasing H₂O; hydrolysis breaks bonds using H₂O.",
                            "Starch (amylose/amylopectin) and glycogen store glucose in compact, insoluble granules.",
                            "Competitive inhibitors increase K_m without changing V_max; non-competitive inhibitors reduce V_max."
                        ],
                        "Explain how glycogen structure relates to its storage function in animal liver and muscle cells.",
                        "1. α-glucose polymer: easily hydrolysed to release glucose for respiration.\n2. Highly branched (1,6-glycosidic bonds): multiple terminal ends for rapid simultaneous enzymatic cleavage.\n3. Insoluble: does not alter cellular osmotic potential.\n4. Compact helical structure: maximizes energy storage density.",
                        [
                            ("Describe the non-reducing sugar biochemical test.", "Boil sample with dilute HCl to hydrolyse glycosidic bonds, neutralise with NaHCO₃, re-test with Benedict's reagent; brick-red precipitate indicates positive result."),
                            ("Contrast competitive and non-competitive enzyme inhibitors.", "Competitive bind active site reversibly (overcome by high [S]); non-competitive bind allosteric site altering 3D conformation (lowers V_max).")
                        ]
                    ),
                    make_topic(
                        "B2", "Cell Structure, Transport and Immunology", "cell-structure-transport-and-immunology",
                        "Ultrastructure of eukaryotic and prokaryotic cells, fluid mosaic membranes, co-transport, cell-mediated and humoral immunity.",
                        [
                            ("Fluid Mosaic Model", "Phospholipid bilayer with lateral mobility of lipids and embedded mosaic of transport/receptor proteins."),
                            ("Antigen", "A cell-surface glycoprotein or macromolecule that triggers an immune response.")
                        ],
                        [
                            "Transport: simple diffusion (small/non-polar), facilitated diffusion (channels/carriers), active transport (ATP against gradient), co-transport (Na⁺-glucose in ileum).",
                            "Humoral immunity: B-cells differentiate into plasma cells producing specific monoclonal antibodies.",
                            "Cell-mediated immunity: cytotoxic T-cells destroy virus-infected and cancerous cells via perforins."
                        ],
                        "Explain the co-transport of glucose in the mammalian ileum epithelium.",
                        "1. Na⁺/K⁺ ATPase actively pumps Na⁺ out of epithelial cell into bloodstream, lowering intracellular [Na⁺].\n2. Na⁺ diffuses down gradient from lumen into cell via sodium-glucose co-transporters, dragging glucose against its gradient.\n3. Glucose exits into capillary blood via facilitated diffusion.",
                        [
                            ("Compare TEM and SEM electron microscopes.", "TEM: transmits electrons through ultra-thin section (2D internal ultrastructure, 0.1 nm resolution). SEM: scans electron beam across surface (3D topography, 20 nm resolution)."),
                            ("Describe the role of memory B-cells in secondary immune response.", "Memory B-cells circulate in blood; upon re-exposure to antigen, they rapidly divide into plasma cells producing high antibody titers before symptoms develop.")
                        ]
                    )
                ]
            },
            {
                "strand": "Physiology, Genetics and Ecology",
                "topics": [
                    make_topic(
                        "B3", "Respiration, Photosynthesis and Bioenergetics", "respiration-photosynthesis-and-bioenergetics",
                        "Glycolysis, Krebs cycle, oxidative phosphorylation, light-dependent and light-independent photosynthetic reactions.",
                        [
                            ("Chemiosmosis", "ATP synthesis driven by proton electrochemical gradient across inner mitochondrial/thylakoid membrane through ATP synthase."),
                            ("Photolysis", "Light-dependent splitting of water in PSII: 2H₂O → 4H⁺ + 4e⁻ + O₂.")
                        ],
                        [
                            "Glycolysis: glucose → 2 pyruvate, net 2 ATP, 2 NADH (cytoplasm).",
                            "Krebs cycle: acetyl-CoA oxidized producing 2 CO₂, 3 NADH, 1 FADH₂, 1 ATP per turn (mitochondrial matrix).",
                            "Calvin cycle (stroma): RuBisCO fixes CO₂ to RuBP (5C) → 2 GP (3C) → reduced to 2 TP (3C) using ATP and NADPH."
                        ],
                        "Explain why oxygen is essential for aerobic ATP production.",
                        "Oxygen acts as the terminal electron acceptor at complex IV of the electron transport chain. It combines with electrons and protons to form H₂O (½O₂ + 2H⁺ + 2e⁻ → H₂O), maintaining electron flow and proton gradient across the inner mitochondrial membrane.",
                        [
                            ("What happens to the Calvin cycle in prolonged darkness?", "Without light-dependent ATP and NADPH, GP cannot be reduced to TP. GP accumulates while RuBP and TP levels drop, halting glucose synthesis."),
                            ("Calculate the respiratory quotient (RQ) for tripalmitin C₅₁H₉₈O₆ + 145/2 O₂ → 51 CO₂ + 49 H₂O.", "RQ = CO₂ produced / O₂ consumed = 51 / 72.5 = 0.70.")
                        ]
                    ),
                    make_topic(
                        "B4", "Genetics, Gene Expression and Recombinant DNA", "genetics-gene-expression-and-recombinant-dna",
                        "Transcription, translation, epigenetic regulation, stem cells, PCR, gel electrophoresis, CRISPR gene editing.",
                        [
                            ("Epigenetics", "Heritable changes in gene expression without changes to the underlying DNA base sequence (e.g. DNA methylation, histone acetylation)."),
                            ("PCR", "Polymerase Chain Reaction: in vitro DNA amplification via denaturation (95°C), annealing (55°C), extension (72°C).")
                        ],
                        [
                            "DNA methylation (adds -CH₃ to cytosine CpG islands) condenses chromatin, silencing gene transcription.",
                            "Histone acetylation loosens chromatin (euchromatin), allowing RNA polymerase access and activating transcription.",
                            "Recombinant DNA tools: reverse transcriptase (mRNA → cDNA), restriction endonucleases (sticky ends), DNA ligase (annealing)."
                        ],
                        "Describe the role of primers and Taq polymerase in PCR.",
                        "1. Primers: short single-stranded DNA sequences that bind complementarily to the 3' ends of target DNA during annealing (55°C), providing a starting double-stranded segment for DNA synthesis.\n2. Taq polymerase: thermostable DNA polymerase (from Thermus aquaticus) that synthesises complementary strands by adding dNTPs at 72°C without denaturing at 95°C.",
                        [
                            ("Distinguish totipotent, pluripotent, and multipotent stem cells.", "Totipotent: can differentiate into all body cells plus extra-embryonic tissues (zygote). Pluripotent: all adult somatic cell types (embryonic). Multipotent: limited range of related cells (e.g. bone marrow hematopoiesis)."),
                            ("Explain how siRNA silences specific target genes.", "siRNA unwinds, binds RISC protein complex, guides it to complementary mRNA sequence, and RISC cleaves the mRNA, preventing translation.")
                        ]
                    )
                ]
            }
        ]
    },

    # 4. Chemistry
    {
        "name": "Chemistry",
        "slug": "chemistry",
        "category": "Sciences",
        "strands": [
            {
                "strand": "Physical and Inorganic Chemistry",
                "topics": [
                    make_topic(
                        "C1", "Thermodynamics and Born-Haber Cycles", "thermodynamics-and-born-haber-cycles",
                        "Lattice enthalpy, Born-Haber cycles, entropy (ΔS), Gibbs free energy (ΔG = ΔH - TΔS), feasibility of reactions.",
                        [
                            ("Lattice Enthalpy", "Enthalpy change when one mole of solid ionic lattice forms from gaseous ions under standard conditions (exothermic)."),
                            ("Gibbs Free Energy", "ΔG = ΔH - TΔS. A reaction is thermodynamically feasible when ΔG ≤ 0.")
                        ],
                        [
                            "Born-Haber: ΔH_f = ΔH_at(metal) + IE(metal) + ΔH_at(non-metal) + EA(non-metal) + ΔH_latt.",
                            "Discrepancy between theoretical (ionic model) and experimental Born-Haber lattice enthalpies indicates covalent character due to polarization.",
                            "ΔG ≤ 0 temperature threshold: T = ΔH / ΔS (ensure units match: J/mol vs kJ/mol)."
                        ],
                        "For CaCO₃(s) → CaO(s) + CO₂(g), ΔH = +178 kJ/mol, ΔS = +161 J/(K·mol). Calculate the temperature above which decomposition is feasible.",
                        "Feasible when ΔG ≤ 0 => T ≥ ΔH / ΔS.\nΔH = 178,000 J/mol.\nT = 178,000 / 161 = 1105.6 K (833°C).",
                        [
                            ("Why is lattice enthalpy of MgO much more exothermic than NaCl?", "Mg²⁺ and O²⁻ have higher charges (+2/-2 vs +1/-1) and smaller ionic radii, generating much stronger electrostatic forces."),
                            ("Explain why dissolving ammonium nitrate in water is endothermic yet spontaneous.", "ΔH > 0 but solid-to-aqueous dissolution greatly increases entropy (ΔS >> 0). At 298 K, TΔS > ΔH, making ΔG = ΔH - TΔS < 0.")
                        ]
                    ),
                    make_topic(
                        "C2", "Equilibria, Kp, pH and Buffer Solutions", "equilibria-kp-ph-and-buffer-solutions",
                        "Gas equilibria Kp, acid-base theories, pH calculations, Ka, Kw, buffer mechanisms, titration curves.",
                        [
                            ("Buffer Solution", "A solution that maintains approximately constant pH when small quantities of acid or base are added."),
                            ("Acid Dissociation Constant (Ka)", "Ka = [H⁺][A⁻]/[HA]; pKa = -log₁₀ Ka.")
                        ],
                        [
                            "Kp expressions use partial pressures: pA = (mole fraction A) × P_total. Temperature is the only variable that alters Kp.",
                            "Weak acid pH: [H⁺] ≈ √(Ka · [HA]) => pH = -log₁₀[H⁺].",
                            "Buffer pH: [H⁺] = Ka · ([HA]/[A⁻]) => pH = pKa + log₁₀([A⁻]/[HA])."
                        ],
                        "Calculate the pH of a buffer with 0.20 M ethanoic acid (Ka = 1.74 × 10⁻⁵) and 0.15 M sodium ethanoate.",
                        "[H⁺] = Ka × ([HA]/[A⁻]) = (1.74 × 10⁻⁵) × (0.20 / 0.15) = 2.32 × 10⁻⁵ M.\npH = -log₁₀(2.32 × 10⁻⁵) = 4.63.",
                        [
                            ("Explain buffer action when small HCl is added to CH₃COOH/CH₃COO⁻.", "Added H⁺ reacts with ethanoate ions: CH₃COO⁻ + H⁺ → CH₃COOH. Equilibrium shifts left, removing excess H⁺ and keeping pH stable."),
                            ("Calculate the pH of 0.050 M Ba(OH)₂ at 298 K (Kw = 1.0 × 10⁻¹⁴).", "[OH⁻] = 2 × 0.050 = 0.10 M. [H⁺] = 1.0 × 10⁻¹⁴ / 0.10 = 1.0 × 10⁻¹³ M => pH = 13.00.")
                        ]
                    )
                ]
            },
            {
                "strand": "Organic and Analytical Chemistry",
                "topics": [
                    make_topic(
                        "C3", "Aromatic Chemistry and Reaction Mechanisms", "aromatic-chemistry-and-reaction-mechanisms",
                        "Benzene delocalisation stability, electrophilic aromatic substitution, nitration, Friedel-Crafts acylation, amines.",
                        [
                            ("Electrophilic Aromatic Substitution", "Reaction where electrophile replaces H on benzene ring, preserving the stable delocalised π-system."),
                            ("Delocalisation Energy", "152 kJ/mol extra stability of benzene over theoretical cyclohexa-1,3,5-triene.")
                        ],
                        [
                            "Evidence against Kekule model: hydrogenation enthalpy (-208 kJ/mol vs -360 kJ/mol), equal C-C bond lengths (0.139 nm), lack of addition reactions.",
                            "Nitration electrophile NO₂⁺ generated via: HNO₃ + 2H₂SO₄ ⇌ NO₂⁺ + 2HSO₄⁻ + H₃O⁺.",
                            "Friedel-Crafts acylation uses RCOCl with AlCl₃ catalyst to form acylium ion R-C⁺=O."
                        ],
                        "Outline the mechanism for electrophilic nitration of benzene to nitrobenzene.",
                        "1. Generation: HNO₃ + 2H₂SO₄ → NO₂⁺ + 2HSO₄⁻ + H₃O⁺.\n2. Attack: Benzene π-electrons attack NO₂⁺ forming arenium intermediate carbocation (horseshoe delocalised over 5 carbons).\n3. Deprotonation: HSO₄⁻ removes H⁺ from sp³ carbon, restoring aromatic ring: Arenium + HSO₄⁻ → Nitrobenzene + H₂SO₄.",
                        [
                            ("Why is phenol more reactive than benzene?", "Lone pair on oxygen partially delocalises into benzene π-system, increasing electron density and activating ring toward electrophiles."),
                            ("Order the basicity of phenylamine, ammonia, ethylamine.", "Ethylamine > Ammonia > Phenylamine. Ethyl group is electron-donating (+I); phenylamine delocalises N lone pair into ring.")
                        ]
                    ),
                    make_topic(
                        "C4", "Organic Synthesis and Spectroscopic Analysis", "organic-synthesis-and-spectroscopic-analysis",
                        "¹H and ¹³C NMR spectroscopy, Infrared spectroscopy, High-resolution Mass Spectrometry, synthetic routes.",
                        [
                            ("Chemical Shift (δ)", "Resonant frequency position relative to TMS standard at δ = 0 ppm in ppm."),
                            ("Spin-Spin Splitting", "(n+1) rule: proton signal split into n+1 peaks by n non-equivalent adjacent protons.")
                        ],
                        [
                            "IR key absorptions: O-H alcohol (broad 3200-3600 cm⁻¹), O-H acid (very broad 2500-3300 cm⁻¹), C=O carbonyl (sharp 1680-1750 cm⁻¹).",
                            "¹³C NMR: number of distinct signals = number of unique carbon environments.",
                            "High-resolution MS: accurate m/z to 4 decimal places distinguishes compounds with same integer mass."
                        ],
                        "Identify C₃H₆O₂ showing IR 1715 cm⁻¹, broad 2500-3300 cm⁻¹, ¹H NMR triplet δ 1.1 (3H), quartet δ 2.4 (2H), singlet δ 11.5 (1H).",
                        "1. IR: 1715 cm⁻¹ (C=O) + 2500-3300 cm⁻¹ (acid O-H) => carboxylic acid (-COOH).\n2. ¹H NMR: δ 11.5 singlet is -COOH proton.\n3. Triplet δ 1.1 (3H) and quartet δ 2.4 (2H) indicates ethyl group CH₃CH₂-.\nStructure: Propanoic acid (CH₃CH₂COOH).",
                        [
                            ("Why is TMS used as NMR standard?", "Single sharp peak at δ = 0 ppm, inert, non-toxic, volatile (easily evaporated)."),
                            ("Describe the D₂O shake in ¹H NMR.", "D₂O exchanges with labile -OH and -NH protons (R-OH + D₂O → R-OD + HOD), causing their signals to disappear from the spectrum.")
                        ]
                    )
                ]
            }
        ]
    },

    # 5. Physics
    {
        "name": "Physics",
        "slug": "physics",
        "category": "Sciences",
        "strands": [
            {
                "strand": "Particles, Waves and Quantum Physics",
                "topics": [
                    make_topic(
                        "P1", "Particle Physics and Quantum Phenomena", "particle-physics-and-quantum-phenomena",
                        "Quarks, leptons, fundamental forces, conservation laws, photoelectric effect, wave-particle duality, de Broglie relation.",
                        [
                            ("Photoelectric Effect", "Emission of electrons from metal surface when irradiated with EM radiation above threshold frequency f₀."),
                            ("Work Function (Φ)", "Minimum photon energy required to liberate an electron from metal surface: hf₀ = Φ.")
                        ],
                        [
                            "Hadrons = Baryons (3 quarks: proton uud, neutron udd) + Mesons (quark-antiquark). Leptons = fundamental (e⁻, μ⁻, τ⁻, neutrinos).",
                            "Photoelectric equation: hf = Φ + E_k(max) = hf₀ + ½mv_max².",
                            "De Broglie wavelength: λ = h / p = h / (mv)."
                        ],
                        "Light of f = 1.2 × 10¹⁵ Hz hits zinc (Φ = 4.3 eV). Find max kinetic energy in eV (h = 6.63 × 10⁻³⁴ J·s).",
                        "Photon energy E = hf = (6.63 × 10⁻³⁴)(1.2 × 10¹⁵) = 7.956 × 10⁻¹⁹ J = 4.97 eV.\nE_k(max) = hf - Φ = 4.97 - 4.30 = 0.67 eV (1.07 × 10⁻¹⁹ J).",
                        [
                            ("State quark transformation in β⁻ decay.", "Down quark changes to up quark via weak interaction: d → u + e⁻ + ν̄_e."),
                            ("Calculate de Broglie wavelength of electron (m = 9.11 × 10⁻³¹ kg) accelerated through 150 V.", "E_k = 1.6 × 10⁻¹⁹ × 150 = 2.4 × 10⁻¹⁷ J. p = √(2mE_k) = 6.61 × 10⁻²⁴ kg m/s => λ = h/p = 0.10 nm.")
                        ]
                    ),
                    make_topic(
                        "P2", "Waves, Optics and Superposition", "waves-optics-and-superposition",
                        "Progressive and stationary waves, Young's double-slit experiment, diffraction gratings, refractive index, total internal reflection.",
                        [
                            ("Superposition Principle", "When two waves meet, the resultant displacement is the vector sum of individual displacements."),
                            ("Coherence", "Waves with constant phase difference and identical frequency/wavelength.")
                        ],
                        [
                            "Double slit fringe spacing: w = λD / s (fringe separation w, slit spacing s, screen distance D).",
                            "Diffraction grating equation: d sin θ = nλ (d = grating spacing = 1/N lines per metre).",
                            "Snell's law: n₁ sin θ₁ = n₂ sin θ₂; Critical angle sin θ_c = n₂ / n₁ (for n₁ > n₂)."
                        ],
                        "Laser light (λ = 632.8 nm) is incident on a grating with 300 lines/mm. Find angle of 2nd order maximum.",
                        "d = 1 / (300 × 10³) = 3.333 × 10⁻⁶ m.\nd sin θ = nλ => sin θ = (2 × 632.8 × 10⁻⁹) / (3.333 × 10⁻⁶) = 0.3797.\nθ = arcsin(0.3797) = 22.3°.",
                        [
                            ("Explain how stationary waves are formed on a stretched string.", "Two identical progressive waves travelling in opposite directions with equal frequency and amplitude superpose, creating nodes (zero displacement) and antinodes (maximum displacement)."),
                            ("Calculate critical angle for glass (n = 1.52) to air (n = 1.00).", "sin θ_c = 1.00 / 1.52 = 0.6579 => θ_c = 41.1°.")
                        ]
                    )
                ]
            },
            {
                "strand": "Fields, Nuclear and Thermal Physics",
                "topics": [
                    make_topic(
                        "P3", "Gravitational, Electric and Magnetic Fields", "gravitational-electric-and-magnetic-fields",
                        "Newton's gravitation, Coulomb's law, electric potential, magnetic flux, Faraday's and Lenz's laws, circular orbit dynamics.",
                        [
                            ("Faraday's Law", "Induced emf is proportional to rate of change of magnetic flux linkage: ε = -N(dΦ/dt)."),
                            ("Lenz's Law", "Direction of induced emf opposes the change in flux causing it.")
                        ],
                        [
                            "Gravitational: F = GMm/r², V_g = -GM/r. Electric: F = q₁q₂/(4πε₀r²), V_E = q/(4πε₀r).",
                            "Charged particle in B-field: Bqv = mv²/r => orbital radius r = mv / (Bq).",
                            "Uniform E-field: E = V/d, F = qE = qV/d."
                        ],
                        "Find the orbital radius of a geostationary satellite (T = 24 hrs, M_earth = 5.97 × 10²⁴ kg).",
                        "GMm/r² = m(2π/T)² r => r³ = GMT² / (4π²).\nr³ = (6.67 × 10⁻¹¹ × 5.97 × 10²⁴ × 86400²) / (4π²) = 7.54 × 10²² m³ => r = 4.22 × 10⁷ m (42,200 km).",
                        [
                            ("Derive escape velocity from planet mass M, radius R.", "½mv² - GMm/R = 0 => v_esc = √(2GM/R)."),
                            ("A 200-turn coil of area 0.05 m² rotates in 0.4 T field at 50 Hz. Find peak emf.", "ε_max = NABω = 200 × 0.4 × 0.05 × (2π × 50) = 1257 V (1.26 kV).")
                        ]
                    ),
                    make_topic(
                        "P4", "Nuclear Physics, Radioactivity and Thermal Physics", "nuclear-physics-radioactivity-and-thermal-physics",
                        "Radioactive decay law, binding energy, nuclear fission/fusion, ideal gas laws, kinetic theory, specific heat capacity.",
                        [
                            ("Binding Energy", "Energy required to disassemble a nucleus into its constituent protons and neutrons (E = Δm c²)."),
                            ("Decay Law", "Activity A = λN; N(t) = N₀ e^{-λt}; half-life t_{1/2} = ln 2 / λ.")
                        ],
                        [
                            "Rutherford scattering: evidence for tiny, dense, positively charged nucleus.",
                            "Ideal gas equation: pV = nRT = NkT; Kinetic theory: pV = ⅓Nm(c_rms)²; mean KE = ³/₂kT.",
                            "Thermal energy: Q = mcΔθ (heating) and Q = mL (phase change)."
                        ],
                        "Calculate the binding energy per nucleon of Helium-4 (mass defect Δm = 0.0304 u, 1 u = 931.5 MeV).",
                        "Total binding energy = 0.0304 × 931.5 MeV = 28.32 MeV.\n4 nucleons => Binding energy per nucleon = 28.32 / 4 = 7.08 MeV/nucleon.",
                        [
                            ("Carbon-14 has half-life 5730 years. A sample has 25% original activity. Find age.", "25% = (½)² => 2 half-lives elapsed = 2 × 5730 = 11,460 years."),
                            ("Calculate the root-mean-square speed of nitrogen molecules (m = 4.65 × 10⁻²⁶ kg) at 300 K (k = 1.38 × 10⁻²³ J/K).", "½m(c_rms)² = ³/₂kT => c_rms = √(3kT/m) = √(3 × 1.38×10⁻²³ × 300 / 4.65×10⁻²⁶) = 517 m/s.")
                        ]
                    )
                ]
            }
        ]
    },

    # 6. Computer Science
    {
        "name": "Computer Science",
        "slug": "computer-science",
        "category": "Sciences",
        "strands": [
            {
                "strand": "Systems and Architecture",
                "topics": [
                    make_topic(
                        "CS1", "Processor Architecture and Operating Systems", "processor-architecture-and-operating-systems",
                        "Von Neumann vs Harvard, Fetch-Decode-Execute cycle, ALU, registers, pipelining, RISC vs CISC, memory management.",
                        [
                            ("Von Neumann Architecture", "Computer architecture where instructions and data share the same memory space and system bus."),
                            ("Pipelining", "Instruction execution technique where multiple instruction phases (Fetch, Decode, Execute) overlap concurrently.")
                        ],
                        [
                            "Registers: PC (Program Counter), MAR (Memory Address), MDR (Memory Data), CIR (Current Instruction), ACC (Accumulator).",
                            "RISC (simple single-cycle instructions, more RAM, pipelining friendly) vs CISC (complex hardware instructions, compact code).",
                            "Operating system roles: Process scheduling (Round Robin, SRT), virtual memory (paging/segmentation), interrupt handling."
                        ],
                        "Explain the Fetch-Decode-Execute cycle step-by-step with register transfers.",
                        "1. Fetch: PC contents copied to MAR (MAR ← [PC]). PC incremented (PC ← [PC] + 1). Instruction fetched from RAM via data bus into MDR (MDR ← [[MAR]]). Instruction moved to CIR (CIR ← [MDR]).\n2. Decode: CIR splits instruction into opcode and operand; Control Unit decodes.\n3. Execute: ALU executes arithmetic/logic or data is loaded/stored; flags updated."
                    )
                ]
            },
            {
                "strand": "Algorithms and Data Structures",
                "topics": [
                    make_topic(
                        "CS2", "Data Structures, Algorithms and Complexity", "data-structures-algorithms-and-complexity",
                        "Stacks, queues, linked lists, binary search trees, Big-O notation, Dijkstra's algorithm, sorting (Merge, Quick, Bubble).",
                        [
                            ("Big-O Notation", "Mathematical classification of algorithmic efficiency in terms of time and space scaling with input size n."),
                            ("Dijkstra's Algorithm", "Single-source shortest path algorithm on weighted graphs using a priority queue.")
                        ],
                        [
                            "Time complexities: Binary search O(log n), Merge sort O(n log n), Bubble/Insertion sort O(n²), Hash table lookup O(1).",
                            "Data structures: Stack (LIFO: push/pop), Queue (FIFO: enqueue/dequeue), BST (left < node < right).",
                            "Graph traversals: Depth-First Search (DFS using stack/recursion), Breadth-First Search (BFS using queue)."
                        ],
                        "Trace a binary search for target 18 in array [2, 5, 8, 12, 16, 18, 24, 30].",
                        "Array length 8, indices 0..7.\n1. mid = (0+7)//2 = 3 (val = 12). 18 > 12 => search right half [4..7].\n2. mid = (4+7)//2 = 5 (val = 18). 18 == 18 => Target found at index 5. (2 comparisons total)."
                    )
                ]
            }
        ]
    },

    # 7. Economics
    {
        "name": "Economics",
        "slug": "economics",
        "category": "Social Sciences",
        "strands": [
            {
                "strand": "Microeconomics",
                "topics": [
                    make_topic(
                        "EC1", "Market Mechanisms, Elasticity and Market Failure", "market-mechanisms-elasticity-and-market-failure",
                        "Price mechanism, PED, YED, XED, market failure, externalities, public goods, government intervention and failure.",
                        [
                            ("Price Elasticity of Demand (PED)", "%Δ in Quantity Demanded / %Δ in Price. Measures consumer responsiveness to price changes."),
                            ("Negative Externality", "A cost imposed on a third party external to the market transaction (Social Cost > Private Cost).")
                        ],
                        [
                            "PED: Elastic (|PED| > 1), Inelastic (|PED| < 1), Unitary (|PED| = 1).",
                            "Public goods characteristics: Non-excludable (free-rider problem) and non-rivalrous in consumption.",
                            "Government intervention tools: Pigouvian taxes, subsidies, maximum/minimum price controls, tradable pollution permits."
                        ],
                        "Using a diagrammatic explanation, show why negative production externalities lead to overproduction in a free market.",
                        "In a free market, output is determined where Marginal Private Benefit (MPB) = Marginal Private Cost (MPC) at Q_market.\nExternal cost (MEC) means Marginal Social Cost (MSC = MPC + MEC) lies above MPC.\nThe social optimum occurs where MSB = MSC at Q_optimum.\nBecause Q_market > Q_optimum, the market overproduces, generating a deadweight welfare loss triangle."
                    )
                ]
            },
            {
                "strand": "Macroeconomics",
                "topics": [
                    make_topic(
                        "EC2", "Macroeconomic Policy, Inflation and Globalisation", "macroeconomic-policy-inflation-and-globalisation",
                        "Aggregate Demand and Supply (AD/AS), fiscal, monetary, and supply-side policies, Phillips curve, international trade.",
                        [
                            ("Aggregate Demand (AD)", "Total spending on domestic output: AD = C + I + G + (X - M)."),
                            ("Monetary Policy", "Central bank actions managing interest rates (base rate), quantitative easing, and money supply to meet inflation targets.")
                        ],
                        [
                            "Macro policy objectives: 2.0% CPI inflation, sustainable GDP growth, low unemployment, balanced current account.",
                            "Short-run Phillips curve shows inverse trade-off between inflation and unemployment; vertical Long-Run Phillips curve at NRU.",
                            "Comparative advantage: countries gain from trade by specializing in goods with lowest opportunity cost."
                        ],
                        "Explain the transmission mechanism of a central bank interest rate hike on aggregate demand.",
                        "1. Higher base rate increases commercial borrowing costs and mortgage rates.\n2. Consumption (C) falls as saving returns rise and discretionary income drops.\n3. Investment (I) falls as hurdle rates for capital projects increase.\n4. Currency appreciates (hot money inflows), making exports dearer and imports cheaper (X - M falls).\n5. Net result: AD shifts left, dampening economic growth and reducing demand-pull inflationary pressure."
                    )
                ]
            }
        ]
    },

    # 8. Psychology
    {
        "name": "Psychology",
        "slug": "psychology",
        "category": "Social Sciences",
        "strands": [
            {
                "strand": "Core Psychological Approaches and Memory",
                "topics": [
                    make_topic(
                        "PY1", "Social Influence and Memory Models", "social-influence-and-memory-models",
                        "Conformity (Asch), obedience (Milgram), Multi-Store Model (Atkinson-Shiffrin), Working Memory Model (Baddeley & Hitch), eyewitness testimony.",
                        [
                            ("Conformity", "A change in a person's behaviour or opinion as a result of real or imagined group pressure (NSI vs ISI)."),
                            ("Working Memory Model", "Multi-component active memory model comprising Central Executive, Phonological Loop, Visuo-Spatial Sketchpad, Episodic Buffer.")
                        ],
                        [
                            "Asch's line experiment: 75% conformed at least once; variables: group size (peaks at 3 confederates), unanimity, task difficulty.",
                            "Milgram's obedience: 65% administered full 450V lethal shock; situational variables: proximity, uniform, location.",
                            "Loftus and Palmer: misleading post-event information (leading verbs: 'smashed' vs 'hit') significantly alters eyewitness memory reconstruction."
                        ],
                        "Evaluate the Working Memory Model compared to the Multi-Store Model of memory.",
                        "Strengths: Supported by dual-task performance studies (Baddeley) showing concurrent visual and verbal tasks perform well, proving separate slave systems. Clinical evidence from patient KF (impaired verbal memory but intact visual memory).\nLimitations: The Central Executive is poorly specified and vague ('the most important but least understood component'). Does not fully account for long-term memory interactions."
                    )
                ]
            }
        ]
    },

    # 9. History
    {
        "name": "History",
        "slug": "history",
        "category": "Humanities",
        "strands": [
            {
                "strand": "Historical Enquiry and Revolutions",
                "topics": [
                    make_topic(
                        "H1", "Revolutions, Authoritarianism and Historical Historiography", "revolutions-authoritarianism-and-historical-historiography",
                        "Source analysis (provenance, utility, reliability), causes of revolutions, consolidation of authoritarian regimes, historical interpretations.",
                        [
                            ("Historiography", "The study of the methodology and changing interpretations of past historical events by different schools of thought."),
                            ("Source Provenance", "Evaluating author, date, purpose, and context to assess reliability, bias, and historical value.")
                        ],
                        [
                            "Evaluate sources on nature, origin, purpose, and corroboration with contextual historical knowledge.",
                            "Authoritarian consolidation: elimination of political opposition, control of judiciary/media, ideological indoctrination, economic mobilization.",
                            "Historians debate structural socio-economic determinism vs intentionalist/individual leadership roles in revolutions."
                        ],
                        "Assess the relative importance of ideological appeal versus coercive terror in the maintenance of totalitarian power.",
                        "Ideology establishes legitimacy, creates mass consensus (propaganda, youth organizations, social mobilization), and justifies state actions. Conversely, coercive terror (secret police, show trials, penal camps) deters dissent and enforces conformity. Most historians conclude terror maintains power in the short term, but ideological indoctrination creates long-term institutional stability."
                    )
                ]
            }
        ]
    },

    # 10. Geography
    {
        "name": "Geography",
        "slug": "geography",
        "category": "Humanities",
        "strands": [
            {
                "strand": "Physical and Human Systems",
                "topics": [
                    make_topic(
                        "G1", "Water and Carbon Cycles, Hazards and Global Governance", "water-and-carbon-cycles-hazards-and-global-governance",
                        "Hydrological flows, carbon stores, feedback loops, plate tectonics and hazard management, globalization, global governance.",
                        [
                            ("Carbon Sink", "A natural or artificial reservoir that absorbs and stores more carbon than it releases (e.g. tropical rainforests, oceans)."),
                            ("Hazard Vulnerability", "The conditions determined by physical, social, economic, and environmental factors which increase the susceptibility of a community to hazard impacts.")
                        ],
                        [
                            "Positive feedback (e.g. arctic permafrost thaw releases CH₄ accelerating warming); negative feedback (e.g. higher CO₂ stimulates photosynthesis).",
                            "Tectonic hazards: destructive, constructive, conservative plate margins; hazard management via Park model and hazard management cycle.",
                            "Globalisation mechanisms: TNCs, trade blocs (EU, USMCA), containerisation, WTO liberalisation."
                        ],
                        "Explain how deforestation impacts both the local hydrological cycle and the global carbon cycle.",
                        "Hydrological: Reduces interception and evapotranspiration; increases overland surface runoff and soil erosion; leads to flashier river discharge hydrographs and local drought.\nCarbon: Burning/decay of trees releases stored carbon as CO₂; removes an active terrestrial carbon sink; accelerates atmospheric greenhouse gas accumulation and global radiative forcing."
                    )
                ]
            }
        ]
    },

    # 11. English Literature
    {
        "name": "English Literature",
        "slug": "english-literature",
        "category": "Core",
        "strands": [
            {
                "strand": "Drama, Poetry and Critical Theory",
                "topics": [
                    make_topic(
                        "EL1", "Shakespeare, Poetry Traditions and Comparative Criticism", "shakespeare-poetry-traditions-and-comparative-criticism",
                        "Tragedy and comedy conventions, poetic metre, sonnet forms, narrative voice in prose, feminist, Marxist, and psychoanalytic criticism.",
                        [
                            ("Hamartia", "A fatal flaw leading to the downfall of a tragic hero in classical and Shakespearean drama."),
                            ("Free Indirect Discourse", "A narrative technique presenting a character's inner thoughts while retaining third-person narration.")
                        ],
                        [
                            "Shakespearean tragedy: hamartia, hubris, peripeteia (reversal of fortune), anagnorisis (recognition), catharsis.",
                            "Poetic forms: Petrarchan sonnet (octave ABBAABBA + sestet), Shakespearean sonnet (3 quatrains + rhyming couplet in iambic pentameter).",
                            "Critical lenses: Marxist (class struggles and economic power), Feminist (patriarchal oppression), Psychoanalytic (Freudian id/ego/superego, repression)."
                        ],
                        "Analyse how Shakespeare uses dramatic irony in tragedy to heighten audience tension.",
                        "Dramatic irony occurs when the audience possesses critical knowledge unknown to characters onstage. In Othello, the audience hears Iago's soliloquies detailing his malevolent machinations, rendering Othello's trust in 'honest Iago' agonizingly tragic and generating heightened dramatic tension as the inevitable catastrophe approaches."
                    )
                ]
            }
        ]
    },

    # 12. English Language
    {
        "name": "English Language",
        "slug": "english-language",
        "category": "Core",
        "strands": [
            {
                "strand": "Language Diversity and Change",
                "topics": [
                    make_topic(
                        "LA1", "Language Diversity, Sociolects and Child Acquisition", "language-diversity-sociolects-and-child-acquisition",
                        "Dialect and sociolect, gender and language theories, Child Language Acquisition (CLA), historical language change.",
                        [
                            ("Sociolect", "A variety of language associated with a particular social class, group, or subculture."),
                            ("Language Acquisition Device (LAD)", "Chomsky's nativist theory proposing an innate biological mechanism enabling children to learn grammatical rules.")
                        ],
                        [
                            "Gender theories: Deficit model (Lakoff), Dominance model (Zimmerman & West), Difference model (Tannen), Diversity model (Cameron).",
                            "Child language theories: Nativist (Chomsky), Behaviourist (Skinner: imitation/reinforcement), Interactionist (Bruner: LASS scaffolding).",
                            "Language change: prescriptivism (judging language against arbitrary standards) vs descriptivism (observing language use neutrally)."
                        ],
                        "Compare Chomsky's nativist view of language acquisition with Skinner's behaviourist model.",
                        "Skinner argues children acquire language purely via operant conditioning (imitation, reinforcement, association). Chomsky refutes this using the 'poverty of the stimulus' argument: children produce novel grammatical utterances ('virtuous errors' like 'I runned') they never heard, demonstrating an innate Language Acquisition Device (LAD) parsing universal grammar."
                    )
                ]
            }
        ]
    },

    # 13. Business Studies
    {
        "name": "Business Studies",
        "slug": "business-studies",
        "category": "Social Sciences",
        "strands": [
            {
                "strand": "Strategy, Finance and Marketing",
                "topics": [
                    make_topic(
                        "BS1", "Strategic Management, Financial Analysis and Marketing", "strategic-management-financial-analysis-and-marketing",
                        "Ansoff matrix, Porter's generic strategies, ratio analysis (ROCE, gearing, liquidity), investment appraisal (NPV), marketing mix.",
                        [
                            ("Return on Capital Employed (ROCE)", "Operating Profit / Total Capital Employed × 100%. Measures business capital efficiency."),
                            ("Net Present Value (NPV)", "The sum of discounted future cash flows minus initial capital outlay.")
                        ],
                        [
                            "Strategic tools: SWOT, PESTEL, Ansoff's Matrix (Market Penetration, Product Dev, Market Dev, Diversification), Porter's 5 Forces.",
                            "Financial ratios: Current ratio (Current Assets/Current Liabilities), Gearing (Non-current liabilities/Capital employed × 100).",
                            "Operations: Lean production, Just-in-Time (JIT), Total Quality Management (TQM), capacity utilization."
                        ],
                        "Evaluate whether a firm should use Net Present Value (NPV) or Payback Period when choosing capital investment projects.",
                        "NPV is superior because it accounts for the time value of money (discounting future cash flows) and includes all cash flows over the project lifecycle. Payback period ignores cash flows received after the payback threshold and ignores profitability, but is simpler and useful for firms with severe liquidity constraints."
                    )
                ]
            }
        ]
    },

    # 14. Sociology
    {
        "name": "Sociology",
        "slug": "sociology",
        "category": "Social Sciences",
        "strands": [
            {
                "strand": "Sociological Theories and Institutions",
                "topics": [
                    make_topic(
                        "SO1", "Sociological Theories, Education and Crime", "sociological-theories-education-and-crime",
                        "Functionalism, Marxism, Feminism, Postmodernism, educational achievement disparities, crime and deviance theories.",
                        [
                            ("Cultural Capital", "Bourdieu's concept of cultural assets (knowledge, taste, language) passed down by middle-class parents that enhance educational success."),
                            ("Labelling Theory", "Interactionist theory (Becker) stating that deviance is not inherent in an act, but is a consequence of social reactions and labels applied by authority.")
                        ],
                        [
                            "Education perspectives: Functionalist (Durkheim/Parsons: meritocracy, social solidarity), Marxist (Bowles & Gintis: correspondence principle), Interactionist (self-fulfilling prophecy).",
                            "Crime perspectives: Functionalist (Durkheim: safety valve, boundary maintenance; Merton's Strain Theory), Left/Right Realism, Interactionist.",
                            "Family perspectives: Functionalist nuclear family ideal (Murdock) vs feminist critique of domestic labour and patriarchy."
                        ],
                        "Outline and evaluate the Marxist view that education legitimises and reproduces class inequality.",
                        "Bowles and Gintis argue the correspondence principle mirrors workplace hierarchies (subservience, external rewards) in schools. Althusser views education as an Ideological State Apparatus transmitting bourgeois values. Evaluation: Willis's 'Learning to Labour' showed working-class 'lads' actively resisted school ideology, disproving deterministic brainwashing."
                    )
                ]
            }
        ]
    },

    # 15. Law
    {
        "name": "Law",
        "slug": "law",
        "category": "Social Sciences",
        "strands": [
            {
                "strand": "The Legal System and Substantive Law",
                "topics": [
                    make_topic(
                        "LW1", "The English Legal System, Criminal and Tort Law", "the-english-legal-system-criminal-and-tort-law",
                        "Judicial precedent, statutory interpretation, criminal liability (Actus Reus & Mens Rea), tort of negligence (Duty, Breach, Damage).",
                        [
                            ("Stare Decisis", "The legal principle of adhering to established precedent in subsequent similar cases."),
                            ("Mens Rea", "The guilty mind or fault element required for criminal liability (intention or subjective recklessness).")
                        ],
                        [
                            "Statutory interpretation rules: Literal rule, Golden rule, Mischief rule (Heydon's Case), Purposive approach.",
                            "Criminal liability: Actus Reus (conduct/result) + Mens Rea (intention/recklessness) without valid defence = Crime.",
                            "Negligence elements: 1. Duty of care (Caparo / Robinson test). 2. Breach (Blyth reasonable person standard). 3. Damage caused (Barnett 'but for' test) and not too remote (Wagon Mound)."
                        ],
                        "Explain the 'but for' test of causation in tort law with reference to Barnett v Chelsea & Kensington Hospital.",
                        "The 'but for' test establishes factual causation: but for the defendant's negligent breach of duty, would the claimant have suffered the harm? In Barnett, hospital staff negligently sent a sick patient home without examination. The patient died of arsenic poisoning. Evidence showed he would have died even with prompt medical treatment; hence negligence was not the factual cause."
                    )
                ]
            }
        ]
    },

    # 16. Politics
    {
        "name": "Politics",
        "slug": "politics",
        "category": "Social Sciences",
        "strands": [
            {
                "strand": "UK and US Political Systems",
                "topics": [
                    make_topic(
                        "PO1", "UK and US Government, Constitutions and Ideologies", "uk-and-us-government-constitutions-and-ideologies",
                        "UK uncodified constitution, parliamentary sovereignty, US separation of powers, political ideologies (Liberalism, Conservatism, Socialism).",
                        [
                            ("Parliamentary Sovereignty", "The supreme legal authority of the UK Parliament to enact or repeal any law, with no parliament binding its successor."),
                            ("Separation of Powers", "Constitutional doctrine dividing government authority between distinct legislative, executive, and judicial branches with checks and balances.")
                        ],
                        [
                            "UK vs US constitution: UK is uncodified, unentrenched, unitary; US is codified, entrenched, federal.",
                            "Executive checks: US President vetoes legislation; Congress overrides with 2/3 majority; Supreme Court conducts judicial review.",
                            "Core ideologies: Liberalism (individual freedom, toleration), Conservatism (tradition, hierarchy, pragmatism), Socialism (equality, collectivism)."
                        ],
                        "Compare the power of the UK Prime Minister with the US President in domestic policy legislation.",
                        "A UK Prime Minister commanding a parliamentary majority exercises fused legislative-executive power with disciplined party voting, passing domestic programs with relative ease. A US President operates under strict separation of powers and checks and balances; without congressional majorities or bipartisanship, presidential legislative proposals frequently stall."
                    )
                ]
            }
        ]
    },

    # 17. Religious Studies
    {
        "name": "Religious Studies",
        "slug": "religious-studies",
        "category": "Humanities",
        "strands": [
            {
                "strand": "Philosophy of Religion and Ethics",
                "topics": [
                    make_topic(
                        "RS1", "Philosophy of Religion, Ethical Theories and Theology", "philosophy-of-religion-ethical-theories-and-theology",
                        "Ontological and Cosmological arguments, problem of evil (Augustine vs Irenaeus/Hick), Natural Law, Utilitarianism, Kantian ethics.",
                        [
                            ("Teleological Argument", "Argument for God's existence based on evidence of design, purpose, and order in the universe (Paley's Watchmaker)."),
                            ("Categorical Imperative", "Kant's deontological moral command: act only according to maxims you can universalise as universal law.")
                        ],
                        [
                            "Arguments for God: Anselm's Ontological (God is that than which nothing greater can be conceived), Aquinas' 5 Ways (Motion, Cause, Contingency).",
                            "Problem of Evil: Logical (Mackie's inconsistent triad) vs Evidential (Rowe/Paul). Theodicies: Augustinian (privation of good) vs Irenaean (soul-making).",
                            "Ethical theories: Deontological (Kant, Aquinas Natural Law) vs Teleological/Consequentialist (Bentham Act Utilitarianism, Mill Rule Utilitarianism)."
                        ],
                        "Critically assess whether the Irenaean/Hick soul-making theodicy successfully resolves the problem of evil.",
                        "Hick argues the world was created imperfect ('epistemic distance') as an environment for moral and spiritual maturation ('soul-making'). This accounts for natural hazards as challenging stimuli. Critiques: It fails to justify excessive, disproportionate suffering (e.g. child suffering, Holocaust) and relies on universal salvation (escatological justification) which undermines human moral responsibility."
                    )
                ]
            }
        ]
    },

    # 18. Physical Education
    {
        "name": "Physical Education",
        "slug": "physical-education",
        "category": "Creative & Physical",
        "strands": [
            {
                "strand": "Sports Science and Psychology",
                "topics": [
                    make_topic(
                        "PE1", "Biomechanics, Exercise Physiology and Sports Psychology", "biomechanics-exercise-physiology-and-sports-psychology",
                        "Cardiovascular dynamics (VO2 max), energy systems (ATP-PC, glycolytic, aerobic), Newton's laws in sport, arousal theories (Inverted-U).",
                        [
                            ("VO2 Max", "The maximum volume of oxygen an individual can uptake, transport, and utilise per minute during maximal exercise."),
                            ("Inverted-U Theory", "Arousal theory stating performance increases with arousal up to an optimal midpoint, beyond which performance deteriorates.")
                        ],
                        [
                            "Energy systems: ATP-PC (0-10s maximal, alactic), Glycolytic/Lactate (10-60s high intensity), Aerobic (submaximal long duration).",
                            "Biomechanics: projectile trajectory (angle, velocity, release height), Bernoulli principle and Magnus effect in ball spin.",
                            "Psychology: Catastrophe theory, Vealey's sport confidence, Bandura's self-efficacy, Weiner's attribution theory."
                        ],
                        "Explain how the Magnus effect causes a spinning football to swerve in flight.",
                        "When a ball is kicked with topspin or sidespin, the spinning surface drags a boundary layer of air with it. On one side, airflow travels in the same direction as the spin, increasing local air velocity and reducing air pressure (Bernoulli's principle). On the opposite side, air opposes the spin, creating high pressure. The pressure differential creates a perpendicular Magnus force swerving the ball."
                    )
                ]
            }
        ]
    },

    # 19. Media Studies
    {
        "name": "Media Studies",
        "slug": "media-studies",
        "category": "Creative & Physical",
        "strands": [
            {
                "strand": "Media Frameworks and Theory",
                "topics": [
                    make_topic(
                        "MS1", "Media Language, Representation, Industries and Audiences", "media-language-representation-industries-and-audiences",
                        "Semiotics (Barthes), narratology (Todorov), representation (Hall, Gauntlett, Gilroy), industry regulation, audience reception (Hall).",
                        [
                            ("Stuart Hall's Reception Theory", "Media texts are encoded by producers with preferred meanings, but decoded by audiences as Preferred, Negotiated, or Oppositional."),
                            ("Semiotic Denotation and Connotation", "Denotation is the literal meaning of a sign; connotation is the associated cultural and emotional interpretation.")
                        ],
                        [
                            "Media Language: Barthes (semiotic codes), Todorov (narrative equilibrium), Neale (genre repetition and difference).",
                            "Representation: Hall (stereotyping and power), Gauntlett (identity fluidity), Gilroy (postcolonial melancholia), Butler (gender performativity).",
                            "Media Industries: Curran and Seaton (profit vs diversity), Livingstone and Lunt (regulation dilemmas in digital convergence)."
                        ],
                        "Apply Stuart Hall's encoding/decoding model to explain why media texts can provoke oppositional readings.",
                        "Producers encode texts with a dominant/preferred ideology using selective media language. However, audiences bring their own socio-economic background, cultural identity, and personal values to decoding. If an audience member's lived experience or political beliefs conflict directly with the encoded message, they reject the preferred reading and generate an oppositional interpretation."
                    )
                ]
            }
        ]
    },

    # 20. French
    {
        "name": "French",
        "slug": "french",
        "category": "Languages",
        "strands": [
            {
                "strand": "Société et Culture Francophone",
                "topics": [
                    make_topic(
                        "FR1", "La Société Française, Immigration et Culture", "la-societe-francaise-immigration-et-culture",
                        "La famille contemporaine, la cyber-société, le bénévolat, le patrimoine et la musique francophone, l'intégration et la laïcité.",
                        [
                            ("Laïcité", "Principe constitutionnel républicain français de stricte séparation de l'État et des institutions religieuses."),
                            ("Le Bénévolat", "L'engagement volontaire non rémunéré au service de l'intérêt général et des associations caritatives.")
                        ],
                        [
                            "Évolution de la famille: PACS, mariage pour tous (Loi Taubira), familles monoparentales et recomposées.",
                            "Patrimoine culturel: exception culturelle française, quotas musicaux Toubon (40% de chansons francophones à la radio).",
                            "Défis sociétaux: intégration, discrimination à l'embauche, banlieues et fracture sociale."
                        ],
                        "Analysez l'impact de la loi sur le Mariage pour tous (2013) sur la société française.",
                        "La loi Taubira a constitué une avancée majeure pour l'égalité des droits des couples de même sexe en France. Malgré de fortes contestations initiales ('La Manif pour tous'), le mariage homosexuel est aujourd'hui largement accepté dans les mœurs et a permis de moderniser le cadre juridique familial français."
                    )
                ]
            }
        ]
    },

    # 21. Spanish
    {
        "name": "Spanish",
        "slug": "spanish",
        "category": "Languages",
        "strands": [
            {
                "strand": "Sociedad y Cultura Hispánica",
                "topics": [
                    make_topic(
                        "SP1", "Sociedad Hispánica, Tradiciones y Movimientos Sociales", "sociedad-hispanica-tradiciones-y-movimientos-sociales",
                        "Evolución de la familia, el impacto del turismo, igualdad de género y machismo, la música y el cine hispano, la inmigración.",
                        [
                            ("Machismo", "Actitud o comportamiento de prepotencia de los varones respecto de las mujeres arraigado tradicionalmente."),
                            ("El Desempleo Juvenil", "El alto porcentaje de jóvenes en edad de trabajar sin empleo, fenómeno notable en España.")
                        ],
                        [
                            "Cambios sociales en España: secularización, ley del divorcio, matrimonio igualitario (2005), emancipación tardía.",
                            "Patrimonio y fiestas: Día de los Muertos, Las Fallas, La Tomatina, flamenco y patrimonio arquitectónico mudéjar.",
                            "Inmigración: la ruta migratoria del Mediterráneo, integración laboral y enriquecimiento multicultural en el mundo hispanohablante."
                        ],
                        "Explica la importancia del turismo en la economía española y sus desafíos ambientales.",
                        "El turismo representa más del 12% del PIB español y millones de puestos de trabajo. No obstante, plantea graves desafíos: gentrificación, escasez de agua en costas, saturación de infraestructuras y aumento del coste de la vivienda en centros urbanos como Barcelona y Mallorca."
                    )
                ]
            }
        ]
    },

    # 22. German
    {
        "name": "German",
        "slug": "german",
        "category": "Languages",
        "strands": [
            {
                "strand": "Gesellschaft und Geschichte",
                "topics": [
                    make_topic(
                        "GM1", "Gesellschaft im Wandel und Deutsche Geschichte", "gesellschaft-im-wandel-und-deutsche-geschichte",
                        "Familie und Partnerschaft, die digitale Welt, Jugendkultur, Feste und Traditionen, die Wiedervereinigung Deutschlands.",
                        [
                            ("Die Wiedervereinigung", "Der historische Prozess der Vereinigung von BRD und DDR am 3. Oktober 1990."),
                            ("Die Energiewende", "Der Übergang Deutschlands zu nachhaltigen und erneuerbaren Energieträgern.")
                        ],
                        [
                            "Familienstrukturen: Zunahme von Single-Haushalten, Elternzeit für Väter, Betreuungsausbau.",
                            "Kultur und Identität: Berliner Kunstszene, Feste wie das Oktoberfest, Karneval und regionale Brauchtümer.",
                            "Historische Wende: Mauerfall (9. November 1989), Ostalgie, wirtschaftliche Anpassung der neuen Bundesländer."
                        ],
                        "Welche sozialen und wirtschaftlichen Herausforderungen brachte die deutsche Wiedervereinigung mit sich?",
                        "Die Wiedervereinigung 1990 führte zu enormen wirtschaftlichen Strukturbrüchen in den neuen Bundesländern, einschließlich hoher Arbeitslosigkeit durch die Privatisierung der Treuhand. Trotz des 'Solidaritätszuschlags' und großer Investitionen bestehen bis heute Lohn- und Rentenunterschiede zwischen Ost und West fort."
                    )
                ]
            }
        ]
    },

    # 23. Latin
    {
        "name": "Latin",
        "slug": "latin",
        "category": "Languages",
        "strands": [
            {
                "strand": "Latin Language and Classical Authors",
                "topics": [
                    make_topic(
                        "LT1", "Advanced Latin Syntax, Cicero and Virgil", "advanced-latin-syntax-cicero-and-virgil",
                        "Ablative absolute, indirect speech, subjunctive clauses (purpose, result, fearing), dactylic hexameter, Aeneid literary analysis.",
                        [
                            ("Ablative Absolute", "A participial construction in the ablative case functioning as a standalone adverbial clause (noun + participle)."),
                            ("Dactylic Hexameter", "The classical epic metre consisting of six metrical feet (dactyls -uu and spondees --).")
                        ],
                        [
                            "Subjunctive constructions: Purpose (ut/ne + subj), Result (ut + subj with signpost word), Indirect Question, Fearing clauses (ne + subj).",
                            "Gerunds (-ndum verbal noun) and Gerundives (-ndus verbal adjective denoting obligation: Carthago delenda est).",
                            "Virgilian epic themes in the Aeneid: pietas (duty to gods/family/Rome), fate, tragic cost of Roman imperial destiny."
                        ],
                        "Translate and explain the grammatical construction of: 'urbe capta, cives fugerunt'.",
                        "Translation: 'When the city was captured, the citizens fled' (or 'The city having been captured...').\nGrammar: 'urbe capta' is an Ablative Absolute, composed of the noun 'urbe' (ablative feminine singular) and the perfect passive participle 'capta' (ablative feminine singular), expressing time and circumstance independent of the main clause."
                    )
                ]
            }
        ]
    },

    # 24. Art and Design
    {
        "name": "Art and Design",
        "slug": "art-and-design",
        "category": "Creative & Physical",
        "strands": [
            {
                "strand": "Visual Analysis and Studio Practice",
                "topics": [
                    make_topic(
                        "AD1", "Critical Context, Material Exploration and Creative Synthesis", "critical-context-material-exploration-and-creative-synthesis",
                        "Formal elements analysis, modern and contemporary art movements, media experimentation, conceptual portfolio development.",
                        [
                            ("Formal Elements", "The core visual components of an artwork: line, tone, colour, texture, shape, form, space."),
                            ("Contextual Analysis", "Evaluating how cultural, historical, political, and philosophical environments influence artistic intent.")
                        ],
                        [
                            "Art movements: Impressionism, Cubism, Surrealism, Abstract Expressionism, Pop Art, Conceptual Art.",
                            "Assessment objectives: AO1 (Contextual understanding), AO2 (Media experimentation), AO3 (Observational recording), AO4 (Personal response).",
                            "Visual journal development: documentation of iterative creative processes, annotations of critical reflection."
                        ],
                        "Explain how Cubism broke with traditional Renaissance single-point perspective.",
                        "Pioneered by Picasso and Braque, Cubism deconstructed three-dimensional subjects into geometric planes and assembled them simultaneously from multiple viewpoints on a two-dimensional canvas. This rejected the Renaissance illusion of depth and linear perspective, emphasizing the flatness of the picture plane and conceptual representation."
                    )
                ]
            }
        ]
    },

    # 25. Music
    {
        "name": "Music",
        "slug": "music",
        "category": "Creative & Physical",
        "strands": [
            {
                "strand": "Analysis, Harmony and Composition",
                "topics": [
                    make_topic(
                        "MU1", "Western Classical Harmony, Sonata Form and Score Analysis", "western-classical-harmony-sonata-form-and-score-analysis",
                        "Sonata-allegro form, functional diatonic harmony, modulation, cadences, orchestration, score reading.",
                        [
                            ("Sonata Form", "A tripartite musical structure comprising Exposition (Theme 1 in tonic, Theme 2 in dominant), Development, and Recapitulation."),
                            ("Circle of Fifths", "Geometric representation of chromatic relationships among the 12 pitch classes and corresponding key signatures.")
                        ],
                        [
                            "Cadences: Perfect (V-I), Imperfect (I/ii/IV-V), Plagal (IV-I), Interrupted (V-vi).",
                            "Harmonic devices: pedal notes, suspensions (preparation, suspension, resolution), sequence, secondary dominants.",
                            "Orchestral evolution: Baroque basso continuo → Classical balanced strings/woodwinds → Romantic expanded brass/percussion."
                        ],
                        "Explain the tonal structure of the Exposition section in classical Sonata Form in a major key.",
                        "The Exposition begins with the First Subject in the tonic key (I). A transition/bridge section modulates to the dominant key (V). The Second Subject is presented in the dominant key, contrasting in character and mood. The section concludes with a codetta in the dominant key before repeating."
                    )
                ]
            }
        ]
    },

    # 26. Drama and Theatre
    {
        "name": "Drama and Theatre",
        "slug": "drama-and-theatre",
        "category": "Creative & Physical",
        "strands": [
            {
                "strand": "Practitioners and Performance Analysis",
                "topics": [
                    make_topic(
                        "DR1", "Theatre Practitioners, Devising and Textual Interpretation", "theatre-practitioners-devising-and-textual-interpretation",
                        "Stanislavski (Naturalism, System), Brecht (Epic Theatre, Alienation Verfremdungseffekt), Artaud (Theatre of Cruelty), design semiotics.",
                        [
                            ("Verfremdungseffekt", "Brecht's alienation effect designed to prevent emotional immersion and provoke critical intellectual reflection."),
                            ("Emotional Memory", "Stanislavski's acting technique where actors recall past personal emotions to inhabit character truth.")
                        ],
                        [
                            "Brechtian techniques: breaking the 4th wall, episodic structure, didactic songs, placards, visible lighting rig.",
                            "Stanislavski system: 'Magic If', given circumstances, objectives, super-objective, emotional memory, physical action.",
                            "Design elements: semiotics of set, lighting (gels, gobos, intensity), costume color symbolism, directional soundscapes."
                        ],
                        "Explain how a director would use Brecht's 'Verfremdungseffekt' to stage a political play.",
                        "A director would employ harsh, uncolored white lighting, keep stage mechanics and lighting rigs in full view of the audience, instruct actors to address the audience directly, display placards announcing scene outcomes in advance, and intersperse scenes with didactic songs to disrupt emotional catharsis and encourage critical analysis."
                    )
                ]
            }
        ]
    },

    # 27. Accounting
    {
        "name": "Accounting",
        "slug": "accounting",
        "category": "Other",
        "strands": [
            {
                "strand": "Financial and Management Accounting",
                "topics": [
                    make_topic(
                        "AC1", "Financial Statements, Ratio Analysis and Costing", "financial-statements-ratio-analysis-and-costing",
                        "Double-entry bookkeeping, income statements, statements of financial position, marginal costing, break-even, variance analysis.",
                        [
                            ("Double-Entry System", "Every financial transaction affects at least two accounts with equal and opposite Debit and Credit entries (Assets = Liabilities + Equity)."),
                            ("Break-Even Point", "The level of output where total revenue equals total costs: Fixed Costs / Contribution per unit.")
                        ],
                        [
                            "Financial statements: Statement of Profit or Loss (revenue - cost of sales = gross profit; - expenses = net profit); Statement of Financial Position.",
                            "Working capital = Current Assets - Current Liabilities; Acid Test ratio = (Current Assets - Inventory) / Current Liabilities.",
                            "Costing techniques: Marginal costing (variable costs assigned to products, fixed costs treated as period costs) vs Absorption costing."
                        ],
                        "A firm has fixed costs of £60,000, selling price of £25/unit, and variable costs of £10/unit. Calculate break-even output and margin of safety if sales are 5,000 units.",
                        "Contribution per unit = £25 - £10 = £15.\nBreak-even output = £60,000 / £15 = 4,000 units.\nMargin of Safety = Actual Sales - Break-even = 5,000 - 4,000 = 1,000 units (or 20%)."
                    )
                ]
            }
        ]
    },

    # 28. Philosophy
    {
        "name": "Philosophy",
        "slug": "philosophy",
        "category": "Humanities",
        "strands": [
            {
                "strand": "Epistemology and Moral Philosophy",
                "topics": [
                    make_topic(
                        "PH1", "Epistemology, Moral Philosophy and Metaphysics of Mind", "epistemology-moral-philosophy-and-metaphysics-of-mind",
                        "Tripartite definition of knowledge (JTB), Gettier problems, Utilitarianism, Kantian deontology, Substance dualism vs Physicalism.",
                        [
                            ("Justified True Belief (JTB)", "The classical tripartite definition of propositional knowledge: S knows that p iff p is true, S believes that p, and S is justified in believing p."),
                            ("Substance Dualism", "Descartes' metaphysical thesis that mind and body are two distinct fundamental substances: thinking non-extended res cogitans and extended physical res extensa.")
                        ],
                        [
                            "Gettier counter-examples: show justified true beliefs can arise by epistemic luck (e.g. Smith and Jones coins in pocket), proving JTB is insufficient.",
                            "Moral theories: Bentham Act Utilitarianism (hedonic calculus), Mill Rule Utilitarianism (higher/lower pleasures), Kant's categorical imperative, Aristotle's virtue ethics.",
                            "Philosophy of Mind: Dualism (interaction problem), Behaviourism, Mind-Brain Identity Theory, Functionalism."
                        ],
                        "Explain how Edmund Gettier's counter-examples challenge the Tripartite Definition of Knowledge (JTB).",
                        "Gettier constructed scenarios where an agent holds a belief that is both true and justified, yet the truth of the belief is connected to justification only by sheer coincidence/luck (e.g., Smith believes 'The man who will get the job has 10 coins in his pocket', justified regarding Jones, but Smith unexpectedly gets the job and coincidentally also has 10 coins). Because knowledge excludes epistemic luck, JTB is insufficient."
                    )
                ]
            }
        ]
    }
]

def generate_full_topic_page(topic, subject_name, subject_slug, strand_name):
    """Generate rich, complete HTML topic page in GCSE/A-Level format."""
    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": p["q"],
                "acceptedAnswer": {"@type": "Answer", "text": p["a"]}
            } for p in topic["practice"]
        ]
    }
    schema_json = json.dumps(schema_faq, ensure_ascii=False)

    definitions_html = "\n".join([
        f'<div class="key-point"><strong>{d["term"]}:</strong> {d["def"]}</div>'
        for d in topic["definitions"]
    ])

    key_points_html = "\n".join([
        f'<li>{kp}</li>'
        for kp in topic["key_points"]
    ])

    practice_html = "\n".join([
        f'''<div class="question">
  <p><strong>Q{i+1}:</strong> {p["q"]}</p>
  <details style="margin-top: 0.5rem;">
    <summary style="cursor: pointer; color: var(--accent); font-weight: 600;">Show Model Answer</summary>
    <div style="margin-top: 0.5rem; padding: 0.75rem; background: var(--bg-secondary); border-left: 3px solid var(--success); border-radius: 4px;">
      <p><strong>Answer:</strong> {p["a"].replace(chr(10), "<br>")}</p>
    </div>
  </details>
</div>'''
        for i, p in enumerate(topic["practice"])
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<script>/* gcanonical-redirect */(function(){{var p=location.pathname,q=location.search,h=location.hash,m=/^(.*)\\/index\\.html$/.exec(p);if(m){{location.replace(m[1]+"/"+q+h);return}}if(!p.endsWith("/")&&!/\\.[a-z0-9]{{1,10}}$/i.test(p)){{location.replace(p+".html"+q+h)}}}})();</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{topic["title"]} - A-Level {subject_name} Revision Notes</title>
<meta name="description" content="{topic["desc"]} Complete revision notes for A-Level {subject_name}.">
<meta name="keywords" content="A-Level {subject_name}, {topic["title"]}, revision notes, past papers, AQA, Edexcel, OCR, WJEC, CCEA">
<meta property="og:title" content="{topic["title"]} - A-Level {subject_name}">
<meta property="og:description" content="{topic["desc"]} Complete revision notes for A-Level {subject_name}.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://scottrix.github.io/alevelrevise/topics/{subject_slug}/{topic["slug"]}.html">
<link rel="canonical" href="https://scottrix.github.io/alevelrevise/topics/{subject_slug}/{topic["slug"]}.html">
<meta property="og:site_name" content="A-Level Revise">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{topic["title"]}">
<meta name="twitter:description" content="{topic["desc"]}">
<script type="application/ld+json">{schema_json}</script>
<link rel="stylesheet" href="../../style.css">
</head>
<body>
<header class="site-header">
<div class="header-content">
<a href="../../index.html" class="logo">📚 A-Level Revise</a>
<nav class="nav">
<a href="../../index.html#subjects">Subjects</a>
<a href="../../{subject_slug}.html">{subject_name}</a>
</nav>
<button id="theme-toggle" class="theme-btn">🌙</button>
</div>
</header>

<main class="topic-content">
<div class="disclaimer-banner"><strong>A-Level Revision Aid:</strong> This resource is designed to support your revision and may contain errors. If you find a discrepancy with your class teaching, your teacher is correct — please let us know at <a href="mailto:alevelrevise@scott.scottrix.co.uk">alevelrevise@scott.scottrix.co.uk</a>.</div>

<nav class="breadcrumb">
<a href="../../index.html">Home</a> <span>›</span>
<a href="../../{subject_slug}.html">{subject_name}</a> <span>›</span>
<a href="../../{subject_slug}.html#{strand_name.lower().replace(' ', '-')}">{strand_name}</a> <span>›</span>
<span>{topic["title"]}</span>
</nav>

<article class="topic-header">
<h1>{topic["id"]}: {topic["title"]}</h1>
<div class="topic-meta">
<span class="badge foundation">Year 1 / AS</span><span class="badge higher">Year 2 / A-Level</span>
<span class="badge">All Boards (AQA, Edexcel, OCR, WJEC, CCEA)</span>
</div>
<p class="topic-desc">{topic["desc"]}</p>
</article>

<section class="section">
<h2>📋 Key Definitions and Core Concepts</h2>
{definitions_html}
</section>

<section class="section">
<h2>🔍 Key Principles & Specification Requirements</h2>
<ul>
{key_points_html}
</ul>
</section>

<section class="section">
<h2>💡 Worked Example Question</h2>
<div class="example">
<div class="example-title">Exam-Style Question</div>
<p><strong>Question:</strong></p>
<p>{topic["example"]["q"]}</p>
<div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid var(--border);">
<p><strong>Model Solution & Mark Scheme:</strong></p>
<pre style="white-space: pre-wrap; font-family: inherit; color: var(--text-primary);">{topic["example"]["a"]}</pre>
</div>
</div>
</section>

<section class="section">
<h2>❓ Practice Questions & Mark Schemes</h2>
<div class="practice-questions">
{practice_html}
</div>
</section>

<div class="topic-nav">
<a href="../../{subject_slug}.html">← Back to {subject_name} Overview</a>
<a href="../../index.html">All Subjects →</a>
</div>
</main>
</body>
</html>"""

def build_all():
    print("Generating comprehensive A-Level topics, subject pages, and index...")
    
    all_subjects_meta = []
    
    for subj in CURRICULUM:
        sname = subj["name"]
        sslug = subj["slug"]
        scat = subj["category"]
        
        topic_count = sum(len(st["topics"]) for st in subj["strands"])
        all_subjects_meta.append({
            "name": sname,
            "slug": sslug,
            "category": scat,
            "topics_count": topic_count
        })
        
        # Ensure topic directory exists in both sites
        for site in ['alevelrevise', 'alevellessons']:
            topic_dir = BASE / site / 'topics' / sslug
            topic_dir.mkdir(parents=True, exist_ok=True)
            
            topic_sidebar_links = []
            sections_html_parts = []
            
            for strand in subj["strands"]:
                st_name = strand["strand"]
                st_slug = st_name.lower().replace(' ', '-')
                cards_html = []
                
                for t in strand["topics"]:
                    t_slug = t["slug"]
                    t_page_rel = f"topics/{sslug}/{t_slug}.html"
                    
                    html_content = generate_full_topic_page(t, sname, sslug, st_name)
                    (topic_dir / f"{t_slug}.html").write_text(html_content, encoding='utf-8')
                    
                    topic_sidebar_links.append(f'<li><a href="{t_page_rel}">{t["id"]}: {t["title"]}</a></li>')
                    cards_html.append(f'''
      <a href="{t_page_rel}" class="topic-card">
        <span class="topic-id">{t["id"]}</span>
        <span class="topic-name">{t["title"]}</span>
      </a>''')
                
                sections_html_parts.append(f'''
    <section id="{st_slug}" class="section">
      <h2>{st_name} ({len(strand["topics"])} Topics)</h2>
      <div class="topics-grid">
        {"".join(cards_html)}
      </div>
    </section>''')
            
            sidebar_html = "\n".join(topic_sidebar_links)
            sections_html = "\n".join(sections_html_parts)
            
            table_rows = "".join([
                f'<tr><td><a href="#{st["strand"].lower().replace(" ", "-")}">{st["strand"]}</a></td><td>{len(st["topics"])}</td></tr>'
                for st in subj["strands"]
            ])
            
            subject_page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<script>/* gcanonical-redirect */(function(){{var p=location.pathname,q=location.search,h=location.hash,m=/^(.*)\\/index\\.html$/.exec(p);if(m){{location.replace(m[1]+"/"+q+h);return}}if(!p.endsWith("/")&&!/\\.[a-z0-9]{{1,10}}$/i.test(p)){{location.replace(p+".html"+q+h)}}}})();</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>A-Level {sname} - Free Revision Notes</title>
<meta name="description" content="Free A-Level {sname} revision notes. {topic_count} topics across {len(subj["strands"])} strands. Aligned with AQA, Edexcel, OCR, WJEC, and CCEA.">
<meta name="keywords" content="A-Level {sname}, {sname} revision notes, past papers, AQA, Edexcel, OCR, WJEC, CCEA">
<meta property="og:title" content="A-Level {sname} - Free Revision Notes">
<meta property="og:description" content="Free A-Level {sname} revision notes. {topic_count} topics. All exam boards.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://scottrix.github.io/{site}/{sslug}.html">
<link rel="canonical" href="https://scottrix.github.io/{site}/{sslug}.html">
<meta property="og:site_name" content="A-Level Revise">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="A-Level {sname}">
<meta name="twitter:description" content="Free A-Level {sname} revision notes. {topic_count} topics. All exam boards.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-header">
<div class="header-content">
<a href="index.html" class="logo">📚 A-Level Revise</a>
<nav class="nav">
<a href="index.html#subjects">Subjects</a>
<a href="index.html">Home</a>
</nav>
<button id="theme-toggle" class="theme-btn">🌙</button>
</div>
</header>

<div class="sidebar">
  <h3>Topics</h3>
  <ul>
    {sidebar_html}
  </ul>
</div>

<div class="ad-right">
  <div class="ad-unit">Advertisement</div>
</div>

<main class="topic-content">
<div class="disclaimer-banner"><strong>A-Level Revision Aid:</strong> This resource is designed to support your revision and may contain errors. If you find a discrepancy with your class teaching, your teacher is correct — please let us know at <a href="mailto:alevelrevise@scott.scottrix.co.uk">alevelrevise@scott.scottrix.co.uk</a>.</div>

<nav class="breadcrumb">
<a href="index.html">Home</a> <span>›</span>
<span>{sname}</span>
</nav>

<article class="topic-header">
<h1>📐 A-Level {sname}</h1>
<div class="topic-meta">
<span class="badge foundation">Year 1 / AS</span>
<span class="badge higher">Year 2 / A-Level</span>
<span class="badge">All Boards (AQA, Edexcel, OCR, WJEC, CCEA)</span>
</div>
<p class="topic-desc">Complete revision notes for A-Level {sname} covering {topic_count} topics across {len(subj["strands"])} main areas. Aligned with AQA, Edexcel, OCR, WJEC, and CCEA specifications.</p>
</article>

<section class="section">
<h2>📊 Course Overview</h2>
<p>A-Level {sname} covers {len(subj["strands"])} core strands with {topic_count} topics total. Content covers both Year 1 / AS foundation and Year 2 advanced material.</p>
<table class="comparison-table">
<tr><th>Strand</th><th>Topics</th></tr>
{table_rows}
</table>
</section>

{sections_html}
</main>
</body>
</html>"""
            (BASE / site / f"{sslug}.html").write_text(subject_page_html, encoding='utf-8')
        
        print(f"Built {sname}: {topic_count} topics")

    # 2. Write subjects.json
    json_out = {
        "site": "A-Level Revise",
        "description": "Comprehensive A-Level revision notes for all subjects and exam boards",
        "examBoards": ["AQA", "Edexcel", "OCR", "WJEC", "CCEA"],
        "subjects": [
            {
                "name": s["name"],
                "slug": s["slug"],
                "category": s["category"],
                "topics_count": s["topics_count"]
            }
            for s in all_subjects_meta
        ]
    }
    (BASE / 'alevelrevise' / 'subjects.json').write_text(json.dumps(json_out, indent=2), encoding='utf-8')
    (BASE / 'alevellessons' / 'subjects.json').write_text(json.dumps(json_out, indent=2), encoding='utf-8')

    # 3. Update index.html
    import subprocess
    subprocess.run(["python3", str(BASE / "fix_index_complete.py")], check=True)
    print("All 28 subjects and topics fully generated!")

if __name__ == "__main__":
    build_all()
