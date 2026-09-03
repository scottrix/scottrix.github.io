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
{
          "title": "Algebraic Expressions",
          "objectives": [
"Simplify algebraic expressions by collecting like terms",
"Expand single and double brackets using distributive law",
"Factorise quadratic expressions including difference of two squares",
"Manipulate algebraic fractions with numerical and algebraic denominators",
"Apply index laws to simplify expressions with powers",
"Use the factor theorem and remainder theorem for polynomial division"
          ],
          "key": [
"Collecting like terms: only terms with identical variables and powers can be combined",
"Expanding brackets: multiply each term inside by the term outside (FOIL for double brackets)",
"Difference of two squares: a^2 - b^2 = (a + b)(a - b)",
"Perfect square trinomials: a^2 +/- 2ab + b^2 = (a +/- b)^2",
"Factorising by grouping: pair terms to extract common factors",
"Algebraic fractions: factorise numerator and denominator first, then cancel common factors",
"Index laws: xᵃ x xᵇ = xᵃ⁺ᵇ, xᵃ ÷ xᵇ = xᵃ⁻ᵇ, (xᵃ)ᵇ = xᵃᵇ, x⁰ = 1, x⁻ᵃ = 1/xᵃ",
"Polynomial long division: dividend = divisor x quotient + remainder",
"Factor theorem: if f(a) = 0 then (x - a) is a factor of f(x)"
          ],
          "example": "Simplify fully: (2x^2 + 3x - 2)/(x + 2) - (x^2 - 4)/(x - 2)",
          "answer": "Factorise: (2x-1)(x+2)/(x+2) - (x-2)(x+2)/(x-2) = (2x-1) - (x+2) = x - 3",
          "practice": [
"Expand and simplify (3x - 2)(x + 4) - (x - 1)^2",
"Factorise completely: 6x^2 + 13x + 6",
"Simplify: (x^3 - 8)/(x^2 - 4)",
"Divide 2x^3 - 5x^2 + 3x - 1 by (x - 2) using polynomial division",
"Given f(x) = x^3 - 6x^2 + 11x - 6, show (x-1) is a factor and factorise fully",
"Simplify: (2x^2y⁻^3)^3 ÷ (4x⁻¹y^2)^2"
          ],
          "videos": [
{
              "title": "Algebraic Expressions - Overview",
              "url": "https://www.youtube.com/results?search_query=Algebraic+Expressions+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Algebraic Expressions - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Algebraic+Expressions+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Mathematics - Algebraic Expressions",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Mathematics - Algebraic Expressions",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Mathematics - Algebraic Expressions",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Algebraic Expressions",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/algebraic-expressions/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Algebraic Expressions",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Algebraic Expressions",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Algebraic+Expressions",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Quadratic Equations",
          "objectives": [
"Solve quadratic equations by factorising",
"Solve by completing the square",
"Use the quadratic formula for any quadratic",
"Interpret the discriminant to determine number and nature of roots",
"Solve quadratic inequalities graphically and algebraically",
"Form and solve quadratic equations from word problems",
"Understand the relationship between roots and coefficients (sum/product)"
          ],
          "key": [
"Standard form: ax^2 + bx + c = 0 (a != 0)",
"Factorising when a=1: find two numbers with product c and sum b",
"Factorising when a!=1: use AC method or trial and error",
"Completing the square: x^2 + bx = (x + b/2)^2 - (b/2)^2",
"Quadratic formula: x = (-b +/- sqrt(b^2-4ac)) / 2a",
"Discriminant Delta = b^2 - 4ac: Delta > 0 -> two distinct real roots; Delta = 0 -> one repeated root; Delta < 0 -> no real roots",
"Quadratic inequalities: sketch parabola or use sign analysis of factors",
"Sum of roots = -b/a, product of roots = c/a",
"Hidden quadratics: substitute u = x^2, u = eˣ, etc."
          ],
          "example": "Solve 2x^2 - 5x - 3 = 0 and hence solve 2sin^2θ - 5sinθ - 3 = 0 for 0 <= θ < 2pi",
          "answer": "2x^2 - 5x - 3 = (2x+1)(x-3) = 0 -> x = -½ or x = 3. Since sinθ ∈ [-1,1], sinθ = -½ -> θ = 7pi/6, 11pi/6",
          "practice": [
"Solve 3x^2 + 10x - 8 = 0 by factorising",
"Solve x^2 - 6x + 2 = 0 by completing the square",
"Use the quadratic formula for 5x^2 - 3x - 1 = 0, leave in surd form",
"Find the range of k for which kx^2 + 4x + k = 0 has real roots",
"Solve the inequality x^2 - 5x + 6 > 0",
"A rectangle has area 24 cm^2 and perimeter 20 cm. Find its dimensions"
          ],
          "videos": [
{
              "title": "Quadratic Equations - Overview",
              "url": "https://www.youtube.com/results?search_query=Quadratic+Equations+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Quadratic Equations - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Quadratic+Equations+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Mathematics - Quadratic Equations",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Mathematics - Quadratic Equations",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Mathematics - Quadratic Equations",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Quadratic Equations",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/quadratic-equations/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Quadratic Equations",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Quadratic Equations",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Quadratic+Equations",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Coordinate Geometry",
          "objectives": [
"Find the equation of a line given gradient and point, or two points",
"Compute distance between two points and midpoint of a segment",
"Determine parallel and perpendicular lines using gradients",
"Find intersection of two lines algebraically",
"Understand equation of a circle (x-a)^2 + (y-b)^2 = r^2",
"Find tangents and normals to circles and curves",
"Apply coordinate geometry to solve geometric problems"
          ],
          "key": [
"Gradient m = (y₂ - y₁)/(x₂ - x₁)",
"Line equations: y - y₁ = m(x - x₁) or y = mx + c",
"Distance d = sqrt((x₂ - x₁)^2 + (y₂ - y₁)^2)",
"Midpoint M = ((x₁ + x₂)/2, (y₁ + y₂)/2)",
"Parallel lines: equal gradients (m₁ = m₂)",
"Perpendicular lines: product of gradients = -1 (m₁ x m₂ = -1)",
"Circle: (x - a)^2 + (y - b)^2 = r^2, centre (a,b), radius r",
"Circle properties: radius ⟂ tangent, perpendicular bisector of chord passes through centre",
"Intersection: solve simultaneous equations of line and circle/line"
          ],
          "example": "Find the equation of the circle with diameter endpoints A(1,2) and B(5,6). Find the tangent at A.",
          "answer": "Centre = midpoint of AB = (3,4). Radius = half of AB = ½sqrt((5-1)^2+(6-2)^2) = ½sqrt32 = 2sqrt2. Circle: (x-3)^2+(y-4)^2=8. Gradient of radius OA = (2-4)/(1-3)=1. Tangent gradient = -1. Tangent at A: y-2 = -1(x-1) -> y = -x+3",
          "practice": [
"Find the line through (-2,3) perpendicular to 2x + 3y = 6",
"Find intersection of y = 2x - 1 and 3x + y = 7",
"Circle C: (x-2)^2 + (y+1)^2 = 25. Find tangent at (5,3)",
"Points A(1,1), B(4,5), C(6,2). Show triangle ABC is right-angled",
"Find the locus of points equidistant from (2,3) and the line y = -1"
          ],
          "videos": [
{
              "title": "Coordinate Geometry - Overview",
              "url": "https://www.youtube.com/results?search_query=Coordinate+Geometry+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Coordinate Geometry - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Coordinate+Geometry+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Mathematics - Coordinate Geometry",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Mathematics - Coordinate Geometry",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Mathematics - Coordinate Geometry",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Coordinate Geometry",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/coordinate-geometry/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Coordinate Geometry",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Coordinate Geometry",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Coordinate+Geometry",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Differentiation",
          "objectives": [
"Differentiate polynomials, rational and negative powers from first principles",
"Apply sum/difference, product, quotient and chain rules",
"Find gradients of tangents and normals to curves",
"Find and classify stationary points (maxima, minima, inflection)",
"Apply second derivative test for nature of stationary points",
"Solve optimisation problems (max/min area, volume, cost)",
"Use implicit differentiation for curves not in y = f(x) form",
"Understand connected rates of change"
          ],
          "key": [
"Power rule: d/dx(xⁿ) = nxⁿ⁻¹ for all real n",
"Sum/difference: d/dx(f+/-g) = f' +/- g'",
"Product rule: d/dx(fg) = f'g + fg'",
"Quotient rule: d/dx(f/g) = (f'g - fg')/g^2",
"Chain rule: d/dx(f(g(x))) = f'(g(x))·g'(x)",
"Stationary points: f'(x) = 0. Max: f'' < 0; Min: f'' > 0; Inflection: f'' = 0 with sign change",
"Tangent: y - y₁ = f'(x₁)(x - x₁); Normal gradient = -1/f'(x₁)",
"Optimisation: find critical points, check endpoints, justify global max/min",
"Implicit: differentiate term-by-term w.r.t x, solve for dy/dx",
"Connected rates: dy/dt = dy/dx · dx/dt"
          ],
          "example": "Find the stationary points of y = x^3 - 3x^2 - 9x + 5 and determine their nature",
          "answer": "y' = 3x^2 - 6x - 9 = 3(x^2 - 2x - 3) = 3(x-3)(x+1) = 0 -> x = 3 or x = -1. y'' = 6x - 6. At x = 3: y'' = 12 > 0 -> minimum at (3, -22). At x = -1: y'' = -12 < 0 -> maximum at (-1, 10)",
          "practice": [
"Differentiate: xsqrt(x+2) using product rule",
"Find the equation of the normal to y = x^2 - 4x + 3 at x = 2",
"A rectangular box with square base has volume 500 cm^3. Find minimum surface area",
"For x^2 + y^2 = 25, find dy/dx when x = 3 (implicit)",
"Radius of a sphere increases at 0.5 cm/s. Rate of volume increase when r = 10 cm?"
          ],
          "videos": [
{
              "title": "Differentiation - Overview",
              "url": "https://www.youtube.com/results?search_query=Differentiation+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Differentiation - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Differentiation+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Mathematics - Differentiation",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Mathematics - Differentiation",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Mathematics - Differentiation",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Differentiation",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/differentiation/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Differentiation",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Differentiation",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Differentiation",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Integration",
          "objectives": [
"Integrate polynomials, rational and negative powers",
"Use reverse chain rule for composite functions",
"Integrate trigonometric, exponential and logarithmic functions",
"Apply substitution and integration by parts",
"Evaluate definite integrals and find area under curves",
"Find area between two curves",
"Calculate volumes of revolution (disc/washer method)",
"Solve differential equations by separation of variables"
          ],
          "key": [
"Power rule: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C (n != -1)",
"Special: ∫1/x dx = ln|x| + C, ∫eˣ dx = eˣ + C",
"Trig: ∫sin x dx = -cos x + C, ∫cos x dx = sin x + C, ∫sec^2x dx = tan x + C",
"Reverse chain: ∫f'(x)[f(x)]ⁿ dx = [f(x)]ⁿ⁺¹/(n+1) + C",
"Substitution: let u = f(x), dx = du/f'(x), change limits if definite",
"By parts: ∫u dv = uv - ∫v du (LIATE for choosing u)",
"Definite: ∫ₐᵇ f(x)dx = F(b) - F(a), area = ∫|f(x)|dx",
"Area between curves: ∫(top - bottom)dx over intersection interval",
"Volume of revolution: V = pi∫y^2 dx (about x-axis) or pi∫x^2 dy (about y-axis)"
          ],
          "example": "Evaluate ∫₀^2 xsqrt(4 - x^2) dx using substitution u = 4 - x^2",
          "answer": "u = 4 - x^2, du = -2x dx -> x dx = -½ du. Limits: x=0->u=4, x=2->u=0. ∫₄⁰ sqrtu (-½)du = ½∫₀⁴ u^½ du = ½[⅔u^⅔]₀⁴ = ⅓(8) = 8/3",
          "practice": [
"∫(3x^2 - 2x + 5)e^{x^3-x^2+5x} dx",
"∫x cos x dx (by parts)",
"∫₀¹ x/(1+x^2)^2 dx",
"Area between y = x^2 and y = 2x - x^2",
"Volume when y = sqrtx, 0<=x<=4 rotated about x-axis",
"Solve dy/dx = 2xy, y(0)=3"
          ],
          "videos": [
{
              "title": "Integration - Overview",
              "url": "https://www.youtube.com/results?search_query=Integration+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Integration - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Integration+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Mathematics - Integration",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Mathematics - Integration",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Mathematics - Integration",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Integration",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/integration/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Integration",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Integration",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Integration",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Trigonometry",
          "objectives": [
"Use exact values for 0 deg , 30 deg , 45 deg , 60 deg , 90 deg  and radian equivalents",
"Apply compound angle, double angle, and half-angle formulae",
"Solve trigonometric equations in given intervals",
"Prove trigonometric identities",
"Apply sine rule, cosine rule, and area = ½ab sin C",
"Sketch graphs of sin, cos, tan and their transformations",
"Understand inverse trigonometric functions and their domains/ranges",
"Express a sin θ +/- b cos θ in the form R sin(θ +/- α)"
          ],
          "key": [
"Exact values table: sin/cos/tan for 0, pi/6, pi/4, pi/3, pi/2",
"Compound angles: sin(A+/-B), cos(A+/-B), tan(A+/-B)",
"Double angle: sin 2A = 2 sin A cos A, cos 2A = cos^2A - sin^2A = 2cos^2A-1 = 1-2sin^2A",
"R-formula: a sin θ + b cos θ = R sin(θ + α) where R = sqrt(a^2+b^2), tan α = b/a",
"Sine rule: a/sin A = b/sin B = c/sin C (ambiguous case SSA)",
"Cosine rule: a^2 = b^2 + c^2 - 2bc cos A",
"Area = ½ab sin C = ½bc sin A = ½ca sin B",
"Graph transformations: y = a sin(bx + c) + d: amplitude |a|, period 2pi/|b|, phase -c/b, vertical shift d",
"Inverse: arcsin x ∈ [-pi/2, pi/2], arccos x ∈ [0, pi], arctan x ∈ (-pi/2, pi/2)"
          ],
          "example": "Solve 2 sin 2θ = sqrt3 cos θ for 0 <= θ < 2pi",
          "answer": "2(2 sin θ cos θ) = sqrt3 cos θ -> cos θ(4 sin θ - sqrt3) = 0. cos θ = 0 -> θ = pi/2, 3pi/2. sin θ = sqrt3/4 ≈ 0.433 -> θ ≈ 0.448, 2.694",
          "practice": [
"Prove: tan 2θ = 2tan θ/(1 - tan^2θ)",
"Solve 3 cos 2θ + sin θ = 1 for 0 <= θ < 360 deg ",
"Express 3 sin θ + 4 cos θ as R sin(θ + α)",
"In triangle ABC, a=7, b=9, ∠C=60 deg . Find c and area",
"Sketch y = 2 cos(2x - pi/3) for 0 <= x <= 2pi",
"Find exact value: sin(arcsin ⅗ + arccos ⁴/₅)"
          ],
          "videos": [
{
              "title": "Trigonometry - Overview",
              "url": "https://www.youtube.com/results?search_query=Trigonometry+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Trigonometry - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Trigonometry+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Mathematics - Trigonometry",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Mathematics - Trigonometry",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Mathematics - Trigonometry",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Trigonometry",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/trigonometry/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Trigonometry",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Trigonometry",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Trigonometry",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "Further Mathematics",
      "topics": [
{
          "title": "Complex Numbers",
          "objectives": [
"Perform arithmetic with complex numbers in cartesian and polar form",
"Represent complex numbers on the Argand diagram",
"Find modulus and argument of complex numbers",
"Apply de Moivre's theorem for powers and roots",
"Solve polynomial equations with complex roots",
"Understand loci on the Argand diagram (circles, lines, half-lines)",
"Use complex numbers to solve geometric problems"
          ],
          "key": [
"Cartesian form: z = a + bi; Polar form: z = r(cos θ + i sin θ) = re^{iθ}",
"Modulus |z| = sqrt(a^2+b^2); Argument arg(z) = arctan(b/a) (adjust for quadrant)",
"Conjugate: z̄ = a - bi = re^{-iθ}; Properties: z + z̄ = 2a, z z̄ = |z|^2",
"de Moivre: (cos θ + i sin θ)ⁿ = cos nθ + i sin nθ; (re^{iθ})ⁿ = rⁿe^{inθ}",
"n-th roots: r^{1/n} e^{i(θ+2kpi)/n} for k = 0,1,...,n-1 (n distinct roots)",
"Complex roots of real polynomials occur in conjugate pairs",
"Loci: |z - a| = r (circle), arg(z - a) = α (half-line), |z - a| = |z - b| (perp bisector)",
"Euler's formula: e^{iθ} = cos θ + i sin θ; cos θ = ½(e^{iθ}+e^{-iθ}), sin θ = (e^{iθ}-e^{-iθ})/(2i)"
          ],
          "example": "Solve z^3 = -8. Plot the roots on an Argand diagram and show they form an equilateral triangle",
          "answer": "z^3 = 8e^{ipi} -> z = 2e^{i(pi+2kpi)/3} for k=0,1,2. Roots: 2e^{ipi/3} = 1+isqrt3, 2e^{ipi} = -2, 2e^{i5pi/3} = 1-isqrt3. Distance between any two = sqrt((1-(-2))^2+(sqrt3-0)^2) = sqrt(9+3) = 2sqrt3 -- all equal, equilateral triangle",
          "practice": [
"Express (1+isqrt3)⁶ in polar form",
"Find all solutions to z⁴ = -16",
"Solve z^2 + 4z + 13 = 0, plot roots",
"Show that |z-3| = 2|z+3| is a circle, find its centre and radius",
"If z = cos θ + i sin θ, express cos 3θ in terms of cos θ"
          ],
          "videos": [
{
              "title": "Complex Numbers - Overview",
              "url": "https://www.youtube.com/results?search_query=Complex+Numbers+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Complex Numbers - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Complex+Numbers+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Further Mathematics - Complex Numbers",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Further Mathematics - Complex Numbers",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Further Mathematics - Complex Numbers",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Complex Numbers",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/complex-numbers/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Complex Numbers",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Complex Numbers",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Complex+Numbers",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Matrices",
          "objectives": [
"Perform matrix addition, subtraction and multiplication",
"Find determinants of 2x2 and 3x3 matrices",
"Find inverses of 2x2 and 3x3 matrices using adjugate or row reduction",
"Solve systems of linear equations using inverse matrices",
"Understand singular matrices and consistency of systems",
"Apply matrices to geometric transformations (reflection, rotation, enlargement)",
"Find eigenvalues and eigenvectors of 2x2 matrices",
"Diagonalise symmetric matrices"
          ],
          "key": [
"Multiplication: (AB)_{ij} = Σₖ A_{ik}B_{kj} -- non-commutative, associative, distributive",
"det 2x2: |a b; c d| = ad - bc; det 3x3: cofactor expansion or Sarrus",
"Inverse 2x2: A⁻¹ = (1/det)[d -b; -c a]; 3x3: adj(A)/det(A) via minors/cofactors",
"System AX = B: if det(A) != 0, X = A⁻¹B (unique solution); if det(A) = 0, either no solution or infinite",
"Transformations: reflection in x-axis [1 0; 0 -1], rotation by θ [cosθ -sinθ; sinθ cosθ]",
"Eigenvalues λ: det(A - λI) = 0; Eigenvectors: (A - λI)v = 0",
"Diagonalisation: P⁻¹AP = D (D diagonal) if A has n linearly independent eigenvectors"
          ],
          "example": "Find eigenvalues and eigenvectors of A = [3 2; 1 4]. Diagonalise A",
          "answer": "det(A-λI) = (3-λ)(4-λ)-2 = λ^2-7λ+10 = (λ-5)(λ-2)=0 -> λ=5,2. λ=5: [−2 2; 1 −1]v=0 -> v₁=[1;1]. λ=2: [1 2; 1 2]v=0 -> v₂=[2;−1]. P=[1 2; 1 −1], D=[5 0; 0 2]. Check P⁻¹AP=D",
          "practice": [
"Find det and inverse of [2 1 3; 0 1 4; 5 6 0]",
"Solve using matrix inverse: 2x+y-z=1, x+2y+z=2, 3x-y+2z=3",
"Find matrix for rotation by 90 deg  about origin followed by reflection in y=x",
"Find eigenvalues of [4 1; 2 3] and corresponding eigenvectors",
"Show [1 2; 2 1] is diagonalisable"
          ],
          "videos": [
{
              "title": "Matrices - Overview",
              "url": "https://www.youtube.com/results?search_query=Matrices+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Matrices - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Matrices+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Further Mathematics - Matrices",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Further Mathematics - Matrices",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Further Mathematics - Matrices",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Matrices",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/matrices/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Matrices",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Matrices",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Matrices",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Vectors",
          "objectives": [
"Perform vector operations in 2D and 3D",
"Use scalar (dot) product to find angles and test perpendicularity",
"Use vector (cross) product to find area and normal vectors",
"Find equations of lines in vector and cartesian form",
"Find equations of planes in vector, cartesian and parametric form",
"Calculate distances: point-to-line, point-to-plane, line-to-line, line-to-plane",
"Find intersections of lines and planes",
"Apply vectors to mechanics problems"
          ],
          "key": [
"Vector form: r = a + λb (line), r = a + λb + μc (plane)",
"Dot product: a·b = |a||b|cosθ = a₁b₁+a₂b₂+a₃b₃; perpendicular iff a·b = 0",
"Cross product: axb = |a||b|sinθ n̂ = det[i j k; a₁ a₂ a₃; b₁ b₂ b₃]",
"Area: triangle = ½|axb|; parallelogram = |axb|; volume = |a·(bxc)|",
"Line eqn: r = a + λb; Cartesian: (x-x₁)/l = (y-y₁)/m = (z-z₁)/n",
"Plane eqn: r·n = d (normal n, distance d/|n| from origin) or n₁x+n₂y+n₃z = d",
"Intersection: substitute line into plane, solve for λ",
"Distance point to plane: |ax₀+by₀+cz₀-d|/sqrt(a^2+b^2+c^2); point to line: |bx(a-p)|/|b|"
          ],
          "example": "Find the intersection of line r = [1; 2; 3] + λ[2; -1; 4] with plane 2x - y + 3z = 10",
          "answer": "Substitute: x=1+2λ, y=2-λ, z=3+4λ. 2(1+2λ)-(2-λ)+3(3+4λ)=10 -> 2+4λ-2+λ+9+12λ=10 -> 17λ+9=10 -> λ=1/17. Point: [19/17; 33/17; 55/17]",
          "practice": [
"Find angle between lines r = [1; 0; -1] + λ[2; 1; 3] and r = [0; 1; 1] + μ[1; -2; 2]",
"Find equation of plane through (1,2,3) perpendicular to vector [2; -1; 1]",
"Distance from point (1,2,3) to plane 2x - 3y + 6z = 10",
"Find shortest distance between skew lines r = [1; 0; 0] + λ[1; 1; 0] and r = [0; 1; 1] + μ[0; 1; 1]",
"Volume of tetrahedron with vertices (0,0,0), (1,0,0), (0,2,0), (0,0,3)"
          ],
          "videos": [
{
              "title": "Vectors - Overview",
              "url": "https://www.youtube.com/results?search_query=Vectors+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Vectors - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Vectors+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Further Mathematics - Vectors",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Further Mathematics - Vectors",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Further Mathematics - Vectors",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Vectors",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/vectors/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Vectors",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Vectors",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Vectors",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Polar Coordinates",
          "objectives": [
"Convert between polar (r,θ) and Cartesian (x,y) coordinates",
"Sketch standard polar curves: circles, cardioids, roses, spirals, lemniscates",
"Find area enclosed by polar curves",
"Find tangents to polar curves (horizontal/vertical)",
"Understand symmetry in polar graphs"
          ],
          "key": [
"x = r cos θ, y = r sin θ; r = sqrt(x^2+y^2), tan θ = y/x (check quadrant)",
"r = a (circle centred at origin), r = 2a cos θ (circle on x-axis), r = 2a sin θ (circle on y-axis)",
"r = a(1 + cos θ) (cardioid), r = a cos(nθ) (n-petal rose if n odd, 2n-petal if n even)",
"r = aθ (Archimedean spiral), r^2 = a^2 cos 2θ (lemniscate)",
"Area = ½∫_{α}^{β} r^2 dθ; Area between curves = ½∫(r₁^2 - r₂^2) dθ",
"Tangents: dy/dθ = sin θ dr/dθ + r cos θ, dx/dθ = cos θ dr/dθ - r sin θ; dy/dx = (dy/dθ)/(dx/dθ)",
"Horizontal tangent: dy/dθ = 0 (r cos θ + sin θ dr/dθ = 0); Vertical: dx/dθ = 0"
          ],
          "example": "Find the area enclosed by one petal of r = 2 cos 3θ",
          "answer": "r = 0 when cos 3θ = 0 -> 3θ = pi/2 -> θ = pi/6. One petal from -pi/6 to pi/6. Area = ½∫_{-pi/6}^{pi/6} (2 cos 3θ)^2 dθ = 2∫_{-pi/6}^{pi/6} cos^2 3θ dθ = ∫(1+cos 6θ) dθ = [θ + ⅙ sin 6θ]_{-pi/6}^{pi/6} = pi/3",
          "practice": [
"Convert r = 2 sin θ to Cartesian, identify the curve",
"Sketch r = 1 + 2 cos θ",
"Area inside r = 2 and outside r = 1 + cos θ",
"Find horizontal tangents of r = 2 sin 2θ",
"Area of one loop of r^2 = 4 cos 2θ"
          ],
          "videos": [
{
              "title": "Polar Coordinates - Overview",
              "url": "https://www.youtube.com/results?search_query=Polar+Coordinates+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Polar Coordinates - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Polar+Coordinates+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Further Mathematics - Polar Coordinates",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Further Mathematics - Polar Coordinates",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Further Mathematics - Polar Coordinates",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Polar Coordinates",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/polar-coordinates/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Polar Coordinates",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Polar Coordinates",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Polar+Coordinates",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Hyperbolic Functions",
          "objectives": [
"Define sinh, cosh, tanh, sech, cosech, coth in terms of exponentials",
"Prove and use hyperbolic identities (analogous to trig identities)",
"Differentiate and integrate hyperbolic functions",
"Solve equations involving hyperbolic functions",
"Use inverse hyperbolic functions and their logarithmic forms",
"Apply hyperbolic functions to calculus problems (e.g. catenary)"
          ],
          "key": [
"sinh x = (eˣ - e⁻ˣ)/2, cosh x = (eˣ + e⁻ˣ)/2, tanh x = sinh x/cosh x",
"Identities: cosh^2x - sinh^2x = 1, 1 - tanh^2x = sech^2x, sinh 2x = 2 sinh x cosh x, cosh 2x = cosh^2x + sinh^2x",
"Derivatives: d/dx(sinh x) = cosh x, d/dx(cosh x) = sinh x, d/dx(tanh x) = sech^2x",
"Integrals: ∫sinh x dx = cosh x + C, ∫cosh x dx = sinh x + C, ∫sech^2x dx = tanh x + C",
"Inverse functions: arsinh x = ln(x + sqrt(x^2+1)), arcosh x = ln(x + sqrt(x^2-1)) (x>=1), artanh x = ½ ln((1+x)/(1-x)) (|x|<1)",
"Osborn's rule: trig identity -> hyperbolic by changing sign of sin^2 terms"
          ],
          "example": "Solve 2 cosh x - 3 sinh x = 1",
          "answer": "2(eˣ+e⁻ˣ)/2 - 3(eˣ-e⁻ˣ)/2 = 1 -> eˣ+e⁻ˣ - 1.5(eˣ-e⁻ˣ) = 1 -> -0.5eˣ + 2.5e⁻ˣ = 1 -> multiply 2eˣ: -e^2ˣ + 5 = 2eˣ -> e^2ˣ + 2eˣ - 5 = 0 -> eˣ = -1 +/- sqrt6 -> eˣ = sqrt6 - 1 -> x = ln(sqrt6 - 1)",
          "practice": [
"Prove: cosh 2x = 2cosh^2x - 1 = 1 + 2sinh^2x",
"∫ sinh^2x dx",
"Solve: tanh x = ½",
"Find arsinh(2)",
"Show that the catenary y = cosh x has arc length ∫cosh x dx from a to b"
          ],
          "videos": [
{
              "title": "Hyperbolic Functions - Overview",
              "url": "https://www.youtube.com/results?search_query=Hyperbolic+Functions+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Hyperbolic Functions - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Hyperbolic+Functions+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Further Mathematics - Hyperbolic Functions",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Further Mathematics - Hyperbolic Functions",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Further Mathematics - Hyperbolic Functions",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Hyperbolic Functions",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/hyperbolic-functions/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Hyperbolic Functions",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Hyperbolic Functions",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Hyperbolic+Functions",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "Physics",
      "topics": [
{
          "title": "Mechanics and Motion",
          "objectives": [
"Apply SUVAT equations for constant acceleration",
"Use Newton's three laws of motion for dynamics problems",
"Calculate momentum, impulse, and apply conservation of momentum",
"Analyse work, energy and power including conservation of energy",
"Solve projectile motion problems by separating horizontal/vertical components",
"Analyse circular motion: centripetal force, angular velocity, period",
"Understand moments, couples and equilibrium of rigid bodies",
"Apply Hooke's law and elastic potential energy"
          ],
          "key": [
"SUVAT: v = u + at, s = ut + ½at^2, v^2 = u^2 + 2as, s = ½(u+v)t -- only for constant a",
"Newton's 1st: equilibrium -> net force zero; 2nd: F = ma (vector); 3rd: action-reaction pairs equal/opposite",
"Momentum p = mv; Impulse J = FDeltat = Deltap; Conservation: Σp_before = Σp_after (isolated system)",
"Work W = F·s = Fs cos θ; KE = ½mv^2; GPE = mgh; Elastic PE = ½kx^2; Power = W/t = Fv",
"Projectiles: horizontal v constant, vertical a = -g; range = u^2sin2θ/g, max height = u^2sin^2θ/(2g)",
"Circular: a = v^2/r = ω^2r, F = mv^2/r = mω^2r, ω = 2pi/T = 2pif, v = ωr",
"Moments: M = F x d (perpendicular distance); Couple: two equal/opposite forces separated by d",
"Equilibrium: ΣF = 0 and ΣM = 0; Centre of mass: weighted mean of positions",
"Hooke: F = kx (within limit of proportionality); EPE = ½kx^2 = ½Fx"
          ],
          "example": "A 0.5 kg ball is projected at 20 m/s at 30 deg  to horizontal. Find maximum height, range, and speed at impact",
          "answer": "uₓ = 20cos30 deg  = 10sqrt3 ≈ 17.32 m/s; uᵧ = 20sin30 deg  = 10 m/s. Max height: vᵧ^2 = uᵧ^2 - 2gh -> 0 = 100 - 19.6h -> h = 5.10 m. Time of flight: t = 2uᵧ/g = 20/9.8 = 2.04 s. Range = uₓ x t = 17.32 x 2.04 = 35.3 m. At impact: vᵧ = -10 m/s, v = sqrt(17.32^2 + 10^2) = 20 m/s",
          "practice": [
"A car accelerates from rest at 3 m/s^2 for 8 s. Find final speed and distance",
"A 1200 kg car hits a stationary 800 kg car. They couple. Find speed after impact",
"A projectile launched at 45 deg  has range 100 m. Find initial speed",
"A 2 kg mass moves in a circle of radius 0.5 m at 4 m/s. Find centripetal force",
"A uniform beam 4 m long, mass 20 kg, rests on supports at 0.5 m and 3.5 m from ends. Find reactions"
          ],
          "videos": [
{
              "title": "Mechanics and Motion - Overview",
              "url": "https://www.youtube.com/results?search_query=Mechanics+and+Motion+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Mechanics and Motion - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Mechanics+and+Motion+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Physics - Mechanics and Motion",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Physics - Mechanics and Motion",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Physics - Mechanics and Motion",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Mechanics and Motion",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/mechanics-and-motion/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Mechanics and Motion",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Mechanics and Motion",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Mechanics+and+Motion",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Electricity and Circuits",
          "objectives": [
"Apply Ohm's law and understand I-V characteristics",
"Analyse series and parallel circuits with resistors",
"Calculate power and energy in DC circuits",
"Use Kirchhoff's laws for complex circuits",
"Understand internal resistance and EMF of cells",
"Analyse potential divider circuits",
"Understand AC circuits: RMS values, phase, reactance, impedance",
"Use oscilloscopes to measure voltage, frequency, phase"
          ],
          "key": [
"Ohm: V = IR (ohmic) vs non-ohmic (filament, diode); I-V curves",
"Series: I same, V splits, R_total = ΣR; Parallel: V same, I splits, 1/R_total = Σ1/R",
"Power: P = IV = I^2R = V^2/R; Energy: E = Pt = IVt",
"Kirchhoff 1st (junction): ΣI_in = ΣI_out (charge conservation); 2nd (loop): ΣV = 0 (energy conservation)",
"EMF ε = I(R + r); Terminal PD V = ε - Ir; r = internal resistance",
"Potential divider: V_out = V_in x R₂/(R₁+R₂); used for sensors",
"AC: I = I₀sin(ωt), V = V₀sin(ωt+φ); V_rms = V₀/sqrt2, I_rms = I₀/sqrt2",
"Capacitive reactance Xc = 1/(ωC); Inductive Xl = ωL; Impedance Z = sqrt(R^2+(Xl-Xc)^2)",
"Resonance: Xl = Xc -> Z_min = R, ω₀ = 1/sqrt(LC)"
          ],
          "example": "A 12 V battery with internal resistance 0.5 Ω is connected to a 5.5 Ω resistor. Find current, terminal PD, power delivered to load, and power wasted in battery",
          "answer": "Total R = 6 Ω. I = 12/6 = 2 A. Terminal V = IR_load = 2x5.5 = 11 V. P_load = I^2R = 4x5.5 = 22 W. P_battery = I^2r = 4x0.5 = 2 W. Check: P_total = εI = 24 W = 22+2",
          "practice": [
"Three resistors 2Ω, 3Ω, 6Ω in parallel. Find equivalent resistance",
"In a potential divider, V_in=12V, R₁=2kΩ, R₂=4kΩ. Find V_out",
"An AC supply 230V RMS, 50Hz. Find peak voltage and period",
"A 10 μF capacitor connected to 240V RMS, 50Hz. Find reactance and current",
"At resonance, a series RLC circuit has R=10Ω, L=0.1H. Find C and Q-factor"
          ],
          "videos": [
{
              "title": "Electricity and Circuits - Overview",
              "url": "https://www.youtube.com/results?search_query=Electricity+and+Circuits+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Electricity and Circuits - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Electricity+and+Circuits+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Physics - Electricity and Circuits",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Physics - Electricity and Circuits",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Physics - Electricity and Circuits",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Electricity and Circuits",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/electricity-and-circuits/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Electricity and Circuits",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Electricity and Circuits",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Electricity+and+Circuits",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Waves",
          "objectives": [
"Describe wave properties: amplitude, wavelength, frequency, period, phase",
"Use the wave equation v = fλ",
"Explain superposition, interference (constructive/destructive), standing waves",
"Describe diffraction and single/double slit patterns",
"Understand polarisation of transverse waves",
"Apply the Doppler effect for sound and light",
"Describe optical fibres: total internal reflection, critical angle",
"Understand refractive index and Snell's law"
          ],
          "key": [
"Wave eqn: v = fλ; phase difference Deltaφ = 2piDeltax/λ = 2pift",
"Superposition: y_total = y₁ + y₂; constructive: Deltaφ = 2npi; destructive: Deltaφ = (2n+1)pi",
"Standing waves: nodes (A=0) at fixed ends; antinodes (A=max) at λ/4 intervals",
"Double slit: fringe spacing w = λD/s; single slit: first minima at a sinθ = λ",
"Polarisation: only transverse waves; Malus's law I = I₀cos^2θ",
"Doppler: f' = f(v +/- v_o)/(v ∓ v_s) for sound; Deltaf/f = v/c for light (non-relativistic)",
"TIR: occurs when n₁ > n₂ and θ > θ_c = arcsin(n₂/n₁); optical fibres use TIR",
"Refractive index: n = c/v = c₁/c₂; Snell: n₁sinθ₁ = n₂sinθ₂"
          ],
          "example": "Light of wavelength 500 nm passes through double slits 0.2 mm apart. Fringes observed on screen 2.5 m away. Find fringe spacing",
          "answer": "w = λD/s = (500x10⁻⁹ x 2.5) / (0.2x10⁻^3) = 6.25x10⁻^3 m = 6.25 mm",
          "practice": [
"A wave travels at 340 m/s with frequency 170 Hz. Find wavelength",
"Two coherent sources 1.5 mm apart produce fringes 4 mm apart at 3 m. Find λ",
"Find critical angle for glass-air interface (n_glass = 1.5)",
"A police siren at 800 Hz approaches at 30 m/s. Find frequency heard (v_sound=340 m/s)",
"Explain why sound waves cannot be polarised"
          ],
          "videos": [
{
              "title": "Waves - Overview",
              "url": "https://www.youtube.com/results?search_query=Waves+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Waves - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Waves+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Physics - Waves",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Physics - Waves",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Physics - Waves",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Waves",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/waves/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Waves",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Waves",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Waves",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Particles and Quantum Physics",
          "objectives": [
"Describe the standard model: quarks, leptons, gauge bosons",
"Understand particle interactions: strong, weak, electromagnetic, gravitational",
"Apply conservation laws: charge, baryon number, lepton number, strangeness",
"Use the photon model: E = hf = hc/λ, momentum p = h/λ",
"Explain the photoelectric effect and Einstein's equation",
"Understand wave-particle duality: de Broglie wavelength λ = h/p",
"Describe atomic line spectra and energy levels",
"Understand particle detectors: cloud chamber, bubble chamber, semiconductor detectors"
          ],
          "key": [
"Quarks (u,d,s,c,b,t) in baryons (3) and mesons (q q̄); Leptons (e,μ,τ,νₑ,ν_μ,ν_τ)",
"Interactions: strong (gluons, q-q), weak (W+/-, Z⁰, β decay), EM (γ, charged), gravity (negligible)",
"Conservation: charge, B, L, S in strong/EM; only charge, B-L in weak",
"Photoelectric: hf = φ + KE_max; threshold f₀ = φ/h; no time lag; intensity ∝ number of photons",
"de Broglie: λ = h/p = h/sqrt(2meV) for electrons; diffraction proves wave nature",
"Line spectra: electrons move between discrete levels; emission (excited->ground), absorption (ground->excited)",
"Energy levels: E_n = -13.6/n^2 eV (hydrogen); transitions give DeltaE = hf",
"Detectors: ionisation trails in cloud/bubble chambers; Si detectors measure energy"
          ],
          "example": "Electrons accelerated through 150 V. Find de Broglie wavelength and explain if diffraction observable",
          "answer": "λ = h/sqrt(2meV) = 6.63x10⁻^3⁴ / sqrt(2x9.11x10⁻^3¹x1.6x10⁻¹⁹x150) ≈ 1.0x10⁻¹⁰ m = 0.1 nm. Comparable to atomic spacing -> diffraction observable (e.g. Davisson-Germer)",
          "practice": [
"Energy of photon with λ = 400 nm",
"In β⁻ decay: n -> p + e⁻ + ν̄ₑ. Check conservation laws",
"Find de Broglie λ for electron at 100 eV",
"Explain why photoelectric effect supports photon model over wave model",
"Hydrogen transition n=3->2. Find λ and colour"
          ],
          "videos": [
{
              "title": "Particles and Quantum Physics - Overview",
              "url": "https://www.youtube.com/results?search_query=Particles+and+Quantum+Physics+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Particles and Quantum Physics - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Particles+and+Quantum+Physics+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Physics - Particles and Quantum Physics",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Physics - Particles and Quantum Physics",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Physics - Particles and Quantum Physics",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Particles and Quantum Physics",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/particles-and-quantum-physics/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Particles and Quantum Physics",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Particles and Quantum Physics",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Particles+and+Quantum+Physics",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Thermal Physics",
          "objectives": [
"Distinguish heat, internal energy, and temperature",
"Use specific heat capacity c and specific latent heat L",
"Apply first law: DeltaU = Q + W (sign conventions)",
"Use ideal gas laws: Boyle, Charles, Pressure, Combined, PV = nRT",
"Understand kinetic theory: pressure from molecular collisions",
"Relate microscopic (molecular) to macroscopic (PV=nRT)",
"Calculate root-mean-square speed: c_rms = sqrt(3RT/M)",
"Understand degrees of freedom and equipartition of energy"
          ],
          "key": [
"Internal energy U = Σ(KE + PE) of molecules; Temperature ∝ mean KE per molecule",
"Q = mcDeltaθ (no phase change); Q = mL (phase change); L_fusion, L_vaporisation",
"1st law: DeltaU = Q + W; W = ∫PdV (work done ON gas); Q +ve into system, W +ve on system",
"Ideal gas: pV = nRT = NkT; Boyle p∝1/V (isothermal), Charles V∝T (isobaric), Pressure p∝T (isochoric)",
"Kinetic theory: pV = ⅓Nm<c^2> -> p = ⅓ρ<c^2>; <c^2> = 3RT/M",
"RMS speed: c_rms = sqrt(3RT/M); M = molar mass in kg/mol",
"Degrees of freedom: monatomic 3 (translational); diatomic 5 (+2 rotational) at room temp",
"Equipartition: each quadratic term contributes ½kT per molecule"
          ],
          "example": "2 moles of ideal gas at 300 K compressed isothermally from 0.02 m^3 to 0.01 m^3. Find work done",
          "answer": "Isothermal: W = ∫PdV = ∫(nRT/V)dV = nRT ln(V₂/V₁) = 2x8.31x300xln(0.5) = -3457 J. Work done ON gas = +3457 J",
          "practice": [
"Heat to raise 500 g water from 20 deg C to 80 deg C (c=4180)",
"1 mole gas at 27 deg C, V=0.022 m^3. Find pressure",
"Explain why C_p > C_v for ideal gas",
"RMS speed of N₂ at 300 K (M=0.028 kg/mol)",
"Derive pV = ⅓Nm<c^2> from momentum change on wall"
          ],
          "videos": [
{
              "title": "Thermal Physics - Overview",
              "url": "https://www.youtube.com/results?search_query=Thermal+Physics+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Thermal Physics - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Thermal+Physics+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Physics - Thermal Physics",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Physics - Thermal Physics",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Physics - Thermal Physics",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Thermal Physics",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/thermal-physics/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Thermal Physics",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Thermal Physics",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Thermal+Physics",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "Chemistry",
      "topics": [
{
          "title": "Atomic Structure and Bonding",
          "objectives": [
"Describe atomic structure: subatomic particles, isotopes, electron configuration",
"Explain ionisation energies and trends across periods/down groups",
"Understand ionic, covalent, metallic, and hydrogen bonding",
"Use electronegativity to predict bond polarity and type",
"Describe shapes of molecules using VSEPR theory",
"Understand intermolecular forces: van der Waals, dipole-dipole, hydrogen bonding",
"Relate structure and bonding to physical properties (melting point, conductivity, solubility)"
          ],
          "key": [
"Atomic structure: p⁺, n⁰, e⁻; isotopes = same Z, different A; electron config: 1s^22s^22p⁶...",
"Ionisation energy: increases across period (↑Z_eff), decreases down group (↑shielding, ↑n)",
"Ionic: metal + non-metal, electron transfer, lattice; Covalent: non-metal + non-metal, sharing",
"Electronegativity (Pauling): increases across, decreases down; >1.7 ionic, <0.4 non-polar covalent",
"VSEPR: electron pairs repel; 2bp -> linear, 3bp -> trigonal planar, 4bp -> tetrahedral, lone pairs reduce angles",
"IMFs: London (all molecules, ∝ electrons), dipole-dipole (polar), H-bonding (H on N,O,F)",
"Properties: Giant ionic/covalent/metallic -> high MP; Simple molecular -> low MP; H-bonding -> higher MP/BP"
          ],
          "example": "Explain why H₂O has a higher boiling point than H₂S despite similar molecular mass",
          "answer": "H₂O has H-bonding (O is highly electronegative, lone pairs); H₂S has only dipole-dipole and London forces. H-bonding is much stronger -> more energy to separate molecules -> higher BP",
          "practice": [
"Write electron configuration of Fe^2⁺ (Z=26)",
"Predict shape and bond angle of NH₃, CO₂, SF₆",
"Rank boiling points: CH₄, NH₃, H₂O, HF -- explain",
"Why does MgO have higher MP than NaCl?",
"Explain conductivity of graphite vs diamond"
          ],
          "videos": [
{
              "title": "Atomic Structure and Bonding - Overview",
              "url": "https://www.youtube.com/results?search_query=Atomic+Structure+and+Bonding+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Atomic Structure and Bonding - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Atomic+Structure+and+Bonding+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Chemistry - Atomic Structure and Bonding",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Chemistry - Atomic Structure and Bonding",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Chemistry - Atomic Structure and Bonding",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Atomic Structure and Bonding",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/atomic-structure-and-bonding/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Atomic Structure and Bonding",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Atomic Structure and Bonding",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Atomic+Structure+and+Bonding",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Energetics",
          "objectives": [
"Define standard enthalpy changes: formation, combustion, neutralisation, atomisation",
"Apply Hess's Law to calculate enthalpy changes",
"Use Born-Haber cycles for lattice enthalpies",
"Calculate enthalpy changes from bond enthalpies",
"Understand enthalpy of solution and hydration",
"Use mean bond enthalpies and their limitations",
"Interpret energy level diagrams"
          ],
          "key": [
"Standard conditions: 100 kPa, 298 K, 1 mol dm⁻^3; DeltaH_f deg  elements = 0",
"Hess: DeltaH_total = ΣDeltaH_steps (path independent); Cycle: formation = atomisation + ionisation + electron affinity + lattice",
"Born-Haber: DeltaH_f deg  = DeltaH_atom + ΣIE + ΣEA + DeltaH_lattice (for ionic compounds)",
"Bond enthalpies: DeltaH = Σ(bonds broken) - Σ(bonds formed); mean values, gaseous only",
"Solution: DeltaH_soln = DeltaH_lattice + DeltaH_hydration; hydration exothermic",
"Energy level diagrams: reactants -> products; exo: products lower; endo: products higher"
          ],
          "example": "Use Born-Haber cycle to calculate lattice enthalpy of NaCl given: DeltaH_f deg (NaCl) = -411, DeltaH_at(Na)=+107, DeltaH_at(Cl)=+122, IE(Na)=+496, EA(Cl)=-349 kJ/mol",
          "answer": "DeltaH_f = DeltaH_at(Na) + DeltaH_at(Cl) + IE(Na) + EA(Cl) + LE. -411 = 107 + 122 + 496 - 349 + LE -> LE = -411 - 376 = -787 kJ/mol. Lattice enthalpy = +787 kJ/mol (endothermic to break)",
          "practice": [
"Define standard enthalpy of combustion",
"Calculate DeltaH for reaction using bond enthalpies: H₂ + Cl₂ -> 2HCl",
"Why are mean bond enthalpies less accurate than formation data?",
"Explain trend in hydration enthalpy down Group 1",
"Sketch energy profile for exothermic reaction with catalyst"
          ],
          "videos": [
{
              "title": "Energetics - Overview",
              "url": "https://www.youtube.com/results?search_query=Energetics+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Energetics - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Energetics+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Chemistry - Energetics",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Chemistry - Energetics",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Chemistry - Energetics",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Energetics",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/energetics/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Energetics",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Energetics",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Energetics",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Kinetics and Equilibria",
          "objectives": [
"Explain collision theory and factors affecting rate: concentration, temperature, catalyst, surface area",
"Use Maxwell-Boltzmann distribution to explain temperature effect",
"Derive and use rate equations: rate = k[A]ᵐ[B]ⁿ; determine order experimentally",
"Calculate rate constant k and half-life for 1st order reactions",
"Understand activation energy and Arrhenius equation: k = Ae^(-Ea/RT)",
"Apply Le Chatelier's principle to changes in concentration, pressure, temperature",
"Write Kc and Kp expressions; relate Kp = Kc(RT)^(Deltan)",
"Understand effect of catalysts on rate and equilibrium position"
          ],
          "key": [
"Rate = Delta[conc]/Deltat; collision theory: effective collisions need E >= Ea and correct orientation",
"Maxwell-Boltzmann: at higher T, more molecules exceed Ea -> exponentially more effective collisions",
"Rate law: rate = k[A]ᵐ[B]ⁿ; m,n = order (not necessarily stoichiometric); overall order = m+n",
"1st order: rate = k[A]; t½ = ln2/k (constant); ln[A] = -kt + ln[A]₀",
"Arrhenius: ln k = -Ea/RT + ln A; plot ln k vs 1/T gives slope -Ea/R",
"Le Chatelier: system shifts to oppose change. Conc: shift to consume added; Pressure: shift to fewer gas moles; Temp: exo shifts left on heating",
"Kc = [products]/[reactants] (equilibrium conc, powers = coeffs); Kp uses partial pressures",
"Kp = Kc(RT)^Deltan where Deltan = moles gas products - moles gas reactants",
"Catalyst: lowers Ea, increases rate equally both directions; NO effect on K or equilibrium position"
          ],
          "example": "For N₂ + 3H₂ ⇌ 2NH₃, DeltaH = -92 kJ/mol. Predict effect on yield of: (a) increasing pressure, (b) increasing temperature, (c) adding Fe catalyst",
          "answer": "(a) 4 mol gas -> 2 mol gas: shift right -> higher yield. (b) Exothermic: heating shifts left -> lower yield. (c) Catalyst speeds up both forward/reverse equally -> no effect on yield, reaches equilibrium faster",
          "practice": [
"Rate = k[A][B]^2. If [A] doubled and [B] tripled, rate factor?",
"Half-life of 1st order reaction is 10 min. k = ?",
"For 2SO₂ + O₂ ⇌ 2SO₃, write Kp. If P_total doubled, effect on yield?",
"Why does increasing temperature increase rate constant?",
"Explain why catalyst doesn't change equilibrium constant"
          ],
          "videos": [
{
              "title": "Kinetics and Equilibria - Overview",
              "url": "https://www.youtube.com/results?search_query=Kinetics+and+Equilibria+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Kinetics and Equilibria - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Kinetics+and+Equilibria+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Chemistry - Kinetics and Equilibria",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Chemistry - Kinetics and Equilibria",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Chemistry - Kinetics and Equilibria",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Kinetics and Equilibria",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/kinetics-and-equilibria/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Kinetics and Equilibria",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Kinetics and Equilibria",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Kinetics+and+Equilibria",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Organic Chemistry",
          "objectives": [
"Name and draw structural formulae for alkanes, alkenes, alcohols, halogenoalkanes, carbonyls, carboxylic acids, esters, amines, amides",
"Understand reaction mechanisms: free radical substitution, electrophilic addition, nucleophilic substitution (SN1/SN2), elimination, nucleophilic addition, oxidation/reduction",
"Apply Markovnikov's rule and understand carbocation stability",
"Distinguish primary, secondary, tertiary alcohols and their oxidation products",
"Understand esterification, hydrolysis, and uses of esters",
"Use IR spectroscopy and mass spectrometry for structure determination",
"Plan multi-step syntheses using retrosynthetic analysis"
          ],
          "key": [
"IUPAC: longest chain, number for lowest locants, prefixes for substituents, suffix for functional group",
"Mechanisms: curly arrows show electron pair movement; SN1: carbocation intermediate (3 deg  > 2 deg  > 1 deg ); SN2: concerted backside attack (1 deg  favoured)",
"Markovnikov: H adds to carbon with more H's (forms more stable carbocation)",
"Oxidation: 1 deg  alcohol -> aldehyde -> carboxylic acid; 2 deg  -> ketone; 3 deg  resistant",
"Esters: RCOOR'; formed from acid + alcohol (conc H₂SO₄); hydrolysis: acid or base (saponification)",
"IR: C=O ~1700, O-H ~3300, C-H ~2900 cm⁻¹; MS: M⁺ peak, fragmentation pattern",
"Retrosynthesis: work backwards from target; identify disconnections; choose reagents"
          ],
          "example": "Propose a mechanism for the reaction of 2-methylpropene with HBr",
          "answer": "Electrophilic addition. H⁺ adds to less substituted C (Markovnikov) -> more stable 3 deg  carbocation (CH₃)₃C⁺. Br⁻ attacks carbocation -> 2-bromo-2-methylpropane. Curly arrows: pi bond to H, H-Br bond to Br",
          "practice": [
"Name: CH₃CH₂CH(OH)CH₃",
"Mechanism for SN2 hydrolysis of CH₃CH₂Br with OH⁻",
"Product of oxidation of CH₃CH₂CH₂OH with acidified K₂Cr₂O₇",
"IR peaks for CH₃COOH",
"Retrosynthesis of CH₃CH₂COOCH₂CH₃ from simple precursors"
          ],
          "videos": [
{
              "title": "Organic Chemistry - Overview",
              "url": "https://www.youtube.com/results?search_query=Organic+Chemistry+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Organic Chemistry - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Organic+Chemistry+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Chemistry - Organic Chemistry",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Chemistry - Organic Chemistry",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Chemistry - Organic Chemistry",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Organic Chemistry",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/organic-chemistry/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Organic Chemistry",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Organic Chemistry",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Organic+Chemistry",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Redox and Electrochemistry",
          "objectives": [
"Assign oxidation states using rules",
"Balance redox half-equations and full equations in acidic/alkaline conditions",
"Understand electrochemical cells: half-cells, salt bridge, cell notation",
"Calculate E deg _cell = E deg _cathode - E deg _anode; predict feasibility",
"Apply Nernst equation for non-standard conditions",
"Understand commercial cells: fuel cells, rechargeable batteries",
"Use standard electrode potentials to predict reaction direction"
          ],
          "key": [
"Oxidation = loss of e⁻ (OIL RIG); Oxidation state rules: element=0, Group 1=+1, O=-2 (exc peroxides), H=+1 (exc hydrides)",
"Half-equations: balance atoms (O with H₂O, H with H⁺), then charge with e⁻",
"Cell: anode (oxidation) || cathode (reduction); E deg _cell = E deg _red(cathode) - E deg _red(anode)",
"Feasible if E deg _cell > 0; Equilibrium: E deg _cell = 0.059/n log K at 298K",
"Nernst: E = E deg  - 0.059/n log Q; concentration cells generate voltage from conc difference",
"Fuel cell: H₂ + ½O₂ -> H₂O; H₂ oxidised at anode, O₂ reduced at cathode; high efficiency",
"Rechargeable: Li-ion (LiCoO₂/Li), NiMH, lead-acid; reversible redox"
          ],
          "example": "Calculate E deg  for: Zn | Zn^2⁺ || Cu^2⁺ | Cu. E deg (Zn^2⁺/Zn) = -0.76V, E deg (Cu^2⁺/Cu) = +0.34V. Is reaction spontaneous?",
          "answer": "E deg _cell = 0.34 - (-0.76) = +1.10 V > 0 -> spontaneous. Zn oxidised (anode), Cu^2⁺ reduced (cathode). Reaction: Zn + Cu^2⁺ -> Zn^2⁺ + Cu",
          "practice": [
"Balance in acid: MnO₄⁻ + Fe^2⁺ -> Mn^2⁺ + Fe^3⁺",
"E deg (Ag⁺/Ag) = +0.80V, E deg (Cu^2⁺/Cu) = +0.34V. Which is stronger oxidising agent?",
"Write Nernst equation for Cu | Cu^2⁺(0.1M) || Ag⁺(0.01M) | Ag",
"Why can't E deg  predict reaction rate?",
"Half-reaction for O₂ + 4H⁺ + 4e⁻ in fuel cell"
          ],
          "videos": [
{
              "title": "Redox and Electrochemistry - Overview",
              "url": "https://www.youtube.com/results?search_query=Redox+and+Electrochemistry+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Redox and Electrochemistry - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Redox+and+Electrochemistry+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Chemistry - Redox and Electrochemistry",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Chemistry - Redox and Electrochemistry",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Chemistry - Redox and Electrochemistry",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Redox and Electrochemistry",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/redox-and-electrochemistry/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Redox and Electrochemistry",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Redox and Electrochemistry",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Redox+and+Electrochemistry",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "Biology",
      "topics": [
{
          "title": "Cell Structure and Function",
          "objectives": [
"Describe structure and function of all major eukaryotic organelles",
"Compare prokaryotic and eukaryotic cells in detail",
"Explain membrane structure (fluid mosaic model) and transport mechanisms",
"Describe cell cycle, mitosis, and meiosis with significance",
"Understand cell specialisation and tissue organisation"
          ],
          "key": [
"Nucleus: DNA, nucleolus; Mitochondria: respiration, cristae; RER/SER: protein/lipid synthesis; Golgi: modification, packaging; Lysosomes: hydrolytic enzymes; Chloroplasts: photosynthesis; Vacuole: turgor",
"Prokaryotes: no nucleus, 70S ribosomes, circular DNA, plasmids, cell wall (peptidoglycan); Eukaryotes: 80S ribosomes, linear DNA, membrane-bound organelles",
"Fluid mosaic: phospholipid bilayer, proteins (integral/peripheral), cholesterol, glycoproteins; Transport: simple diffusion, facilitated (channel/carrier), active (Na⁺/K⁺ pump), endo/exocytosis",
"Cell cycle: interphase (G₁,S,G₂), M phase (mitosis: PMAT), cytokinesis; Meiosis: two divisions, crossing over (prophase I), independent assortment -> genetic variation",
"Tissues: groups of similar cells; Organs: multiple tissues; Systems: multiple organs"
          ],
          "example": "Explain how the structure of the mitochondria enables efficient aerobic respiration",
          "answer": "Double membrane: outer permeable, inner folded into cristae (large SA for ETC). Matrix contains Krebs cycle enzymes. Intermembrane space accumulates H⁺ for chemiosmosis. Own DNA/ribosomes for some ETC proteins",
          "practice": [
"Compare 70S vs 80S ribosomes",
"Describe Na⁺/K⁺ pump mechanism",
"Explain significance of crossing over in meiosis I",
"Why do plant cells have larger vacuoles than animal cells?"
          ],
          "videos": [
{
              "title": "Cell Structure and Function - Overview",
              "url": "https://www.youtube.com/results?search_query=Cell+Structure+and+Function+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Cell Structure and Function - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Cell+Structure+and+Function+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Biology - Cell Structure and Function",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Biology - Cell Structure and Function",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Biology - Cell Structure and Function",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Cell Structure and Function",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/cell-structure-and-function/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Cell Structure and Function",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Cell Structure and Function",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Cell+Structure+and+Function",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Genetics and Inheritance",
          "objectives": [
"Describe DNA structure, replication (semi-conservative), and the genetic code",
"Explain transcription, translation, and post-transcriptional modification",
"Apply Mendelian genetics: monohybrid, dihybrid, test crosses",
"Understand gene linkage, crossing over, and epistasis",
"Apply chi-squared test to genetic ratios",
"Describe mutations: gene (point, frameshift) and chromosome (structural, numerical)"
          ],
          "key": [
"DNA: antiparallel strands, complementary base pairing (A-T, G-C), sugar-phosphate backbone; Replication: helicase, DNA polymerase, Okazaki fragments, ligase",
"Transcription: RNA pol, promoter, mRNA; Translation: tRNA, ribosome, codon-anticodon, start/stop codons; Eukaryotes: splicing (introns/exons), 5' cap, poly-A tail",
"Mendel: segregation, independent assortment; Punnett squares; Test cross: unknown x homozygous recessive",
"Linkage: genes on same chromosome; recombination frequency ∝ distance; Epistasis: one gene masks another (e.g. 9:3:4, 12:3:1, 9:7 ratios)",
"Chi-squared: χ^2 = Σ(O-E)^2/E; df = n-1; p>0.05 = accept null (observed = expected)",
"Mutations: substitution (silent/missense/nonsense), insertion/deletion (frameshift); Chromosomal: deletion, duplication, inversion, translocation, non-disjunction"
          ],
          "example": "In sweet peas, flower colour is controlled by two genes (C and P). Both dominant alleles needed for purple flowers. Cross CcPp x CcPp. Find phenotypic ratio",
          "answer": "Both genes needed for purple. C_P_ = purple (9/16); ccP_ = white (3/16); C_pp = white (3/16); ccpp = white (1/16). Ratio = 9 purple : 7 white (complementary epistasis)",
          "practice": [
"Describe semi-conservative replication",
"A cross gives 9:3:3:1. What does this indicate?",
"Chi-squared test: observed 52:18, expected 3:1 ratio. Calculate χ^2",
"Explain how a frameshift mutation affects protein"
          ],
          "videos": [
{
              "title": "Genetics and Inheritance - Overview",
              "url": "https://www.youtube.com/results?search_query=Genetics+and+Inheritance+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Genetics and Inheritance - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Genetics+and+Inheritance+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Biology - Genetics and Inheritance",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Biology - Genetics and Inheritance",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Biology - Genetics and Inheritance",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Genetics and Inheritance",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/genetics-and-inheritance/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Genetics and Inheritance",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Genetics and Inheritance",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Genetics+and+Inheritance",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Biochemistry and Respiration",
          "objectives": [
"Detail glycolysis, link reaction, Krebs cycle, oxidative phosphorylation",
"Explain substrate-level phosphorylation and oxidative phosphorylation (chemiosmosis)",
"Calculate ATP yield per glucose (theoretical vs actual)",
"Describe anaerobic respiration in animals (lactate) and yeast (ethanol)",
"Explain enzyme structure, mechanism (lock-and-key, induced fit), factors affecting activity",
"Understand metabolic pathways regulation: feedback inhibition, allosteric regulation"
          ],
          "key": [
"Glycolysis: glucose -> 2 pyruvate (cytoplasm); net 2 ATP, 2 NADH; Link: pyruvate -> acetyl CoA + CO₂ + NADH (mito matrix); Krebs: acetyl CoA + 3NAD⁺ + FAD + GDP -> 2CO₂ + 3NADH + FADH₂ + GTP; ETC: NADH/FADH₂ -> H⁺ gradient -> ATP synthase -> ATP",
"SLP: direct phosphate transfer (glycolysis, Krebs); OxPhos: H⁺ pumped across inner membrane, flow through ATP synthase",
"Theoretical: 10 NADH (2.5 each) + 2 FADH₂ (1.5 each) + 4 ATP = 32 ATP; Actual ~30-32",
"Anaerobic: animals: pyruvate + NADH -> lactate + NAD⁺ (lactate dehydrogenase); Yeast: pyruvate -> acetaldehyde + CO₂ -> ethanol + NAD⁺",
"Enzymes: globular proteins, active site, specific; Induced fit: substrate binding changes shape; Factors: temp, pH, [substrate], inhibitors (competitive/non-competitive)",
"Feedback inhibition: end product inhibits early enzyme; Allosteric: effector binds site != active site, changes conformation"
          ],
          "example": "Calculate total ATP from one glucose via aerobic respiration. Explain why yield is often less than theoretical",
          "answer": "Glycolysis: 2 ATP + 2 NADH (3-5 ATP); Link: 2 NADH (5 ATP); Krebs: 2 ATP + 6 NADH (15 ATP) + 2 FADH₂ (3 ATP) = 25-30 + 4 = 29-32 ATP. Less because: proton leak, shuttle costs (glycerol-3-P shuttle vs malate-aspartate), ATP for transport",
          "practice": [
"Where does each stage of respiration occur?",
"Why does anaerobic respiration produce less ATP?",
"Explain induced fit model",
"How does cyanide affect respiration?"
          ],
          "videos": [
{
              "title": "Biochemistry and Respiration - Overview",
              "url": "https://www.youtube.com/results?search_query=Biochemistry+and+Respiration+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Biochemistry and Respiration - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Biochemistry+and+Respiration+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Biology - Biochemistry and Respiration",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Biology - Biochemistry and Respiration",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Biology - Biochemistry and Respiration",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Biochemistry and Respiration",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/biochemistry-and-respiration/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Biochemistry and Respiration",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Biochemistry and Respiration",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Biochemistry+and+Respiration",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Ecology and Ecosystems",
          "objectives": [
"Describe energy flow: productivity (GPP, NPP), ecological efficiency, pyramids of number/biomass/energy",
"Explain carbon and nitrogen cycles in detail",
"Understand population dynamics: growth curves, limiting factors, predator-prey cycles",
"Explain succession: primary vs secondary, climax community",
"Understand human impacts: climate change, eutrophication, conservation"
          ],
          "key": [
"GPP = total photosynthesis; NPP = GPP - R (respiration); Efficiency = energy transferred/total available x100% (typically 10%); Pyramids: energy always upright; biomass can be inverted",
"Carbon: photosynthesis, respiration, combustion, decomposition, ocean uptake; Nitrogen: fixation (lightning, bacteria), nitrification (ammonia->nitrite->nitrate), assimilation, denitrification",
"Growth curves: lag, log, stationary, death; Carrying capacity K; r/K selection; Predator-prey: Lotka-Volterra cycles",
"Succession: pioneer -> intermediate -> climax; each stage modifies environment for next; Deflected succession: human interference",
"Climate change: greenhouse effect, CO₂, CH₄; Eutrophication: nitrates/phosphates -> algal bloom -> decomposition -> O₂ depletion -> dead zones"
          ],
          "example": "Explain why only ~10% of energy transfers between trophic levels",
          "answer": "Energy lost as: heat (respiration), faeces (undigested), urine (excretion), uneaten parts. Only energy in consumed biomass available to next level. 2nd law of thermodynamics: entropy increases",
          "practice": [
"Define GPP and NPP",
"Describe nitrogen fixation",
"Draw logistic growth curve, label K and r",
"What is a climax community?",
"Explain ocean acidification mechanism"
          ],
          "videos": [
{
              "title": "Ecology and Ecosystems - Overview",
              "url": "https://www.youtube.com/results?search_query=Ecology+and+Ecosystems+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Ecology and Ecosystems - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Ecology+and+Ecosystems+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Biology - Ecology and Ecosystems",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Biology - Ecology and Ecosystems",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Biology - Ecology and Ecosystems",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Ecology and Ecosystems",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/ecology-and-ecosystems/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Ecology and Ecosystems",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Ecology and Ecosystems",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Ecology+and+Ecosystems",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Homeostasis and the Nervous System",
          "objectives": [
"Explain homeostasis: set point, receptors, effectors, negative/positive feedback",
"Detail kidney structure and osmoregulation (ADH, loop of Henle)",
"Describe nervous system: CNS/PNS, neurone types, resting/action potential, synapses",
"Explain hormonal control: endocrine glands, insulin/glucagon, adrenaline, thyroxine",
"Understand temperature regulation: hypothalamus, vasodilation/constriction, sweating, shivering"
          ],
          "key": [
"Negative feedback: deviation -> correction (e.g. blood glucose, temp, water); Positive: amplifies (e.g. oxytocin in childbirth)",
"Kidney: cortex/medulla; nephron (Bowman's capsule, PCT, loop of Henle, DCT, collecting duct); ADH: increases water permeability of DCT/CD; Loop: counter-current multiplier creates medullary gradient",
"Neurones: sensory, relay, motor; Resting potential -70mV (Na⁺/K⁺ pump, K⁺ leak); Action potential: depolarisation (Na⁺ in), repolarisation (K⁺ out), refractory period",
"Synapse: Ca^2⁺ -> vesicle fusion -> neurotransmitter -> receptor -> depolarisation; Summation: temporal/spatial",
"Hormones: insulin (β-cells, lowers glucose), glucagon (α-cells, raises glucose), adrenaline (fight/flight), thyroxine (metabolic rate); Diabetes: type 1 (no insulin), type 2 (insulin resistance)"
          ],
          "example": "Describe how the loop of Henle creates a water potential gradient in the kidney medulla",
          "answer": "Descending limb: permeable to water, impermeable to ions -> water leaves by osmosis. Ascending limb: impermeable to water, active Na⁺/Cl⁻ transport out -> filtrate diluted, medulla concentrated. Counter-current multiplier: flow in opposite directions maintains gradient",
          "practice": [
"Define homeostasis",
"Explain action potential phases",
"How does insulin lower blood glucose?",
"Role of hypothalamus in thermoregulation",
"Difference between type 1 and type 2 diabetes"
          ],
          "videos": [
{
              "title": "Homeostasis and the Nervous System - Overview",
              "url": "https://www.youtube.com/results?search_query=Homeostasis+and+the+Nervous+System+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Homeostasis and the Nervous System - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Homeostasis+and+the+Nervous+System+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Biology - Homeostasis and the Nervous System",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Biology - Homeostasis and the Nervous System",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Biology - Homeostasis and the Nervous System",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Homeostasis and the Nervous System",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/homeostasis-and-the-nervous-system/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Homeostasis and the Nervous System",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Homeostasis and the Nervous System",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Homeostasis+and+the+Nervous+System",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "English Literature",
      "topics": [
{
          "title": "Poetry Analysis",
          "objectives": [
"Analyse poetic language: imagery, metaphor, simile, personification, symbolism",
"Understand form and structure: stanza, rhyme scheme, metre, enjambment, caesura",
"Interpret tone, mood, and voice",
"Compare poems across themes, techniques, and contexts",
"Write critical appreciations with textual evidence"
          ],
          "key": [
"Metaphor (direct comparison), simile (like/as), personification (human qualities to non-human)",
"Imagery: visual, auditory, tactile, olfactory, gustatory; extended metaphors",
"Sound devices: alliteration, assonance, consonance, onomatopoeia, sibilance",
"Structure: stanza types, rhyme (ABAB, AABB, free verse), metre (iambic, trochaic), line breaks",
"Enjambment (run-on lines), caesura (mid-line pause), volta (turn)",
"Tone: attitude of speaker; Mood: atmosphere created; Voice: persona adopted",
"Themes: love, death, nature, time, identity, power, conflict"
          ],
          "example": "Analyse how the poet uses structure and language to convey the theme of loss in 'When You Are Old' by Yeats",
          "answer": "Three stanzas move from present to past to future. Iambic pentameter creates reflective tone. 'Glad grace' (alliteration) contrasts with 'pilgrim soul' (metaphor). Final stanza 'bending down beside the glowing bars' -- imagery of ageing/regret. ABBA rhyme encloses memory",
          "practice": [
"Identify and explain the effect of caesura in a given line",
"Compare how two poets present nature",
"Analyse an extended metaphor across a poem",
"Discuss how rhyme scheme contributes to meaning",
"Write a paragraph on tone shift in a poem"
          ],
          "videos": [
{
              "title": "Poetry Analysis - Overview",
              "url": "https://www.youtube.com/results?search_query=Poetry+Analysis+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Poetry Analysis - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Poetry+Analysis+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level English Literature - Poetry Analysis",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level English Literature - Poetry Analysis",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level English Literature - Poetry Analysis",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Poetry Analysis",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/poetry-analysis/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Poetry Analysis",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Poetry Analysis",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Poetry+Analysis",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Prose and the Novel",
          "objectives": [
"Analyse characterisation: flat/round, static/dynamic, foils",
"Understand narrative voice: 1st, 3rd limited, 3rd omniscient, unreliable narrator",
"Explore themes through plot, setting, and symbolism",
"Contextualise novels: historical, social, cultural, biographical",
"Evaluate critical interpretations and theoretical approaches"
          ],
          "key": [
"Character: direct/indirect presentation; protagonist/antagonist; character arc",
"Narrative perspective: 1st (intimate, biased), 3rd limited (one consciousness), omniscient (all-knowing), stream of consciousness",
"Setting: time, place, atmosphere; pathetic fallacy; symbolic settings",
"Themes: developed through motifs, recurring images, contrasts, parallels",
"Context: author's life, period (Victorian, Modernist, Postcolonial), reception history",
"Critical lenses: feminist, Marxist, psychoanalytic, postcolonial, eco-critical"
          ],
          "example": "Discuss how the first-person narration in 'The Great Gatsby' shapes our understanding of Gatsby",
          "answer": "Nick as participant-observer creates intimacy but limits access to Gatsby's interiority. His judgement 'Gatsby turned out all right' frames our view. Unreliable moments (drunk at party) and admiration create ambivalence. We see Gatsby through Nick's romanticisation",
          "practice": [
"Compare 1st vs 3rd person narration effects",
"Analyse a character foil pair",
"Discuss symbolic significance of a setting",
"Evaluate a feminist reading of a novel",
"Trace a motif across a text"
          ],
          "videos": [
{
              "title": "Prose and the Novel - Overview",
              "url": "https://www.youtube.com/results?search_query=Prose+and+the+Novel+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Prose and the Novel - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Prose+and+the+Novel+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level English Literature - Prose and the Novel",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level English Literature - Prose and the Novel",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level English Literature - Prose and the Novel",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Prose and the Novel",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/prose-and-the-novel/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Prose and the Novel",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Prose and the Novel",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Prose+and+the+Novel",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Drama and Shakespeare",
          "objectives": [
"Analyse dramatic techniques: soliloquy, aside, dramatic irony, foil, subplot",
"Interpret Shakespearean language: blank verse, prose, imagery, wordplay",
"Evaluate staging: set, lighting, costume, movement, directorial choices",
"Explore themes: power, ambition, love, betrayal, appearance vs reality",
"Understand Elizabethan/Jacobean context and theatrical conventions"
          ],
          "key": [
"Soliloquy: character alone, reveals inner thoughts; Aside: to audience, others don't hear",
"Dramatic irony: audience knows more than characters; creates tension",
"Blank verse: unrhymed iambic pentameter (nobles); Prose: lower status, madness, intimacy",
"Shakespearean imagery: clothing, blood, disease, nature, light/dark",
"Stagecraft: minimal sets, emphasis on language; modern: lighting, sound, multimedia",
"Tragedy: hamartia, peripeteia, anagnorisis, catharsis; Comedy: marriage, mistaken identity"
          ],
          "example": "How does the 'dagger soliloquy' (Macbeth 2.1) reveal Macbeth's state of mind?",
          "answer": "Hallucinated dagger shows guilt before action. 'Is this a dagger which I see before me?' -- rhetorical question. 'Bloody business' -- euphemism. 'Hecate's offer' -- supernatural. 'Words to the heat of deeds too cold breath gives' -- hesitation. Rhyme 'knell/summon' = finality",
          "practice": [
"Analyse dramatic irony in a key scene",
"Compare verse vs prose for a character",
"Discuss how staging affects interpretation",
"Explore the tragic hero archetype",
"Analyse a key image cluster"
          ],
          "videos": [
{
              "title": "Drama and Shakespeare - Overview",
              "url": "https://www.youtube.com/results?search_query=Drama+and+Shakespeare+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Drama and Shakespeare - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Drama+and+Shakespeare+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level English Literature - Drama and Shakespeare",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level English Literature - Drama and Shakespeare",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level English Literature - Drama and Shakespeare",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Drama and Shakespeare",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/drama-and-shakespeare/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Drama and Shakespeare",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Drama and Shakespeare",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Drama+and+Shakespeare",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Critical Writing and Context",
          "objectives": [
"Structure thesis-led essays using PEEL/PEAL paragraphs",
"Select and analyse quotations effectively (not dumping)",
"Integrate context (AO3) without bolt-on paragraphs",
"Evaluate alternative interpretations and critical views",
"Write comparative essays across texts"
          ],
          "key": [
"PEEL: Point, Evidence, Explanation, Link back to question",
"Quote analysis: technique + meaning + effect + link to argument",
"Context: woven into analysis (AO3) not separate; historical, literary, biographical",
"AO5: alternative readings (e.g. feminist, Marxist); critical quotations as springboards",
"Comparison: integrated structure (point by point) not text by text; similarities/differences",
"Exam technique: plan 5 mins, write 45 mins, check 5 mins; answer the question set"
          ],
          "example": "Write a thesis statement for: 'Explore how Shakespeare presents ambition in Macbeth'",
          "answer": "Shakespeare presents ambition as a corrupting force that destroys moral order, using Macbeth's hamartia and Lady Macbeth's manipulation to show how unchecked desire for power leads to tyranny and self-destruction, ultimately restored by divine retribution",
          "practice": [
"Write PEEL paragraph on a given theme",
"Integrate context into a quotation analysis",
"Plan a comparative essay structure",
"Evaluate a critical viewpoint",
"Practise exam timing"
          ],
          "videos": [
{
              "title": "Critical Writing and Context - Overview",
              "url": "https://www.youtube.com/results?search_query=Critical+Writing+and+Context+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Critical Writing and Context - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Critical+Writing+and+Context+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level English Literature - Critical Writing and Context",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level English Literature - Critical Writing and Context",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level English Literature - Critical Writing and Context",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Critical Writing and Context",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/critical-writing-and-context/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Critical Writing and Context",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Critical Writing and Context",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Critical+Writing+and+Context",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "History",
      "topics": [
{
          "title": "Interpretation and Sources",
          "objectives": [
"Evaluate primary and secondary sources using provenance, content, and context",
"Understand historiography: different schools of interpretation (Whig, Marxist, Revisionist, Postmodern)",
"Assess utility and reliability: purpose, audience, bias, corroboration",
"Apply source analysis frameworks (OPVL: Origin, Purpose, Value, Limitation)",
"Build evidence-based arguments acknowledging counter-arguments"
          ],
          "key": [
"Primary: contemporary to event (documents, artefacts, oral testimony); Secondary: later analysis by historians",
"OPVL: Origin (who, when, where), Purpose (why created), Value (what it reveals), Limitation (what it omits/distorts)",
"Reliability: accuracy, bias, typicality; Utility: usefulness for specific enquiry",
"Historiography: Whig (progress), Marxist (class struggle), Revisionist (challenge orthodoxy), Postmodern (multiple truths)",
"Corroboration: cross-reference multiple sources; Triangulation: different types of evidence"
          ],
          "example": "Evaluate the utility of a 1917 Bolshevik poster for a historian studying propaganda in the Russian Revolution",
          "answer": "Origin: Bolshevik party, 1917. Purpose: mobilise support, demonise opponents. Value: reveals Bolshevik messaging, visual rhetoric, target audience (workers/soldiers). Limitation: one-sided, omit failures, not objective. Utility: high for studying propaganda techniques, low for factual accuracy of events",
          "practice": [
"Apply OPVL to a diary entry from WWI",
"Compare two historians' views on the causes of the English Civil War",
"Explain the difference between reliability and utility",
"Identify historiographical school of a given extract",
"Use three sources to corroborate a claim"
          ],
          "videos": [
{
              "title": "Interpretation and Sources - Overview",
              "url": "https://www.youtube.com/results?search_query=Interpretation+and+Sources+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Interpretation and Sources - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Interpretation+and+Sources+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level History - Interpretation and Sources",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level History - Interpretation and Sources",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level History - Interpretation and Sources",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Interpretation and Sources",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/interpretation-and-sources/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Interpretation and Sources",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Interpretation and Sources",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Interpretation+and+Sources",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Themed Study: Key Eras",
          "objectives": [
"Analyse long-term and short-term causes of major historical events",
"Identify and evaluate turning points and their significance",
"Assess change and continuity across extended periods",
"Understand structural vs contingent factors in historical change",
"Compare experiences across regions/social groups"
          ],
          "key": [
"Causes: long-term (structural: economic, social, ideological) vs short-term (triggers, contingent events)",
"Turning points: moments of decisive change; evaluate extent of change vs continuity after",
"Change vs continuity: what changed, what stayed same; rate, direction, depth of change",
"Structural forces: demography, economy, geography; Contingent: individual decisions, accidents, weather",
"Comparative: elites vs ordinary people; centre vs periphery; gender, class, ethnicity perspectives"
          ],
          "example": "To what extent was 1066 a turning point in English history?",
          "answer": "Significant change: Norman elite replaced Anglo-Saxon, feudalism introduced, language (French influence), church reform, castle-building, Domesday Book. Continuity: shire system, common law roots, parish structure, monarchy institution. Assessment: political/cultural rupture but administrative continuity",
          "practice": [
"Analyse causes of the French Revolution: long-term vs short-term",
"Was 1918 a turning point for women in Britain?",
"Compare change/continuity in Tudor religious policy",
"Evaluate significance of the Industrial Revolution for working-class lives",
"Identify structural vs contingent factors in fall of Berlin Wall"
          ],
          "videos": [
{
              "title": "Themed Study: Key Eras - Overview",
              "url": "https://www.youtube.com/results?search_query=Themed+Study:+Key+Eras+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Themed Study: Key Eras - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Themed+Study:+Key+Eras+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level History - Themed Study: Key Eras",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level History - Themed Study: Key Eras",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level History - Themed Study: Key Eras",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Themed Study: Key Eras",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/themed-study:-key-eras/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Themed Study: Key Eras",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Themed Study: Key Eras",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Themed+Study:+Key+Eras",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Depth Study: a Period in Detail",
          "objectives": [
"Construct detailed chronological frameworks",
"Analyse key individuals: agency vs structural constraints",
"Evaluate significance of events, policies, and movements",
"Use detailed factual knowledge to support nuanced arguments",
"Engage with historiographical debates specific to the period"
          ],
          "key": [
"Chronology: precise dates, sequence, duration, contemporaneity",
"Key figures: biography, ideology, agency, constraints, legacy, historiographical reputation",
"Significance: immediate impact, long-term consequences, symbolic importance, scale/depth",
"Nuanced argument: avoid determinism; weigh multiple factors; qualify judgements",
"Debates: e.g. intentionalist vs functionalist (Holocaust), revisionist vs traditional (Cold War)"
          ],
          "example": "Assess the significance of Lenin in the Bolshevik consolidation of power 1917-1924",
          "answer": "Crucial: April Theses redirected party; Oct Revolution leadership; Treaty of Brest-Litovsk (pragmatism); War Communism/NEP (ideological flexibility); suppressed opposition (Cheka, ban on factions). But: structural factors (war, economic collapse, peasant resistance) also critical. Historiography: Service (central) vs Figes (contingent)",
          "practice": [
"Create timeline of key events 1917-1924",
"Evaluate role of Trotsky vs Lenin",
"Debate: was NEP betrayal or necessity?",
"Analyse impact of Kronstadt rebellion",
"Compare Soviet vs Western interpretations"
          ],
          "videos": [
{
              "title": "Depth Study: a Period in Detail - Overview",
              "url": "https://www.youtube.com/results?search_query=Depth+Study:+a+Period+in+Detail+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Depth Study: a Period in Detail - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Depth+Study:+a+Period+in+Detail+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level History - Depth Study: a Period in Detail",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level History - Depth Study: a Period in Detail",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level History - Depth Study: a Period in Detail",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Depth Study: a Period in Detail",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/depth-study:-a-period-in-detail/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Depth Study: a Period in Detail",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Depth Study: a Period in Detail",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Depth+Study:+a+Period+in+Detail",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Historical Enquiry and Essay Skills",
          "objectives": [
"Formulate focused, answerable historical questions",
"Plan and structure analytical essays with sustained argument",
"Select, deploy, and weigh evidence effectively",
"Write balanced conclusions with substantiated judgements",
"Reference and cite sources appropriately"
          ],
          "key": [
"Good question: specific, debatable, evidence-based, manageable scope (not 'Why WWI?' but 'How far did German naval policy cause WWI?')",
"Essay structure: intro (thesis + line of argument), themed paragraphs (PEEL), conclusion (judgement + significance)",
"Evidence: select best, not all; deploy precisely (dates, stats, quotes); weigh (corroboration, provenance)",
"Judgement: 'ultimately', 'more significantly', 'on balance'; avoid fence-sitting; relative significance",
"Citation: footnotes (Chicago) or in-text; bibliography; primary/secondary distinction"
          ],
          "example": "Write an essay introduction for: 'How far was economic crisis the main cause of the French Revolution?'",
          "answer": "The French Revolution (1789) resulted from a convergence of fiscal collapse, social tension, and Enlightenment ideas. While economic crisis -- state bankruptcy, grain shortages, regressive taxation -- provided the immediate catalyst, this essay argues that structural weaknesses of the Ancien Régime (privilege, absolutism, lack of representation) made revolution probable, with Enlightenment providing the intellectual framework. Economic crisis was the spark, not the fuel",
          "practice": [
"Formulate 3 enquiry questions on a topic",
"Plan a 45-min essay",
"Write a conclusion with nuanced judgement",
"Practise weighing two pieces of evidence",
"Reference a primary source correctly"
          ],
          "videos": [
{
              "title": "Historical Enquiry and Essay Skills - Overview",
              "url": "https://www.youtube.com/results?search_query=Historical+Enquiry+and+Essay+Skills+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Historical Enquiry and Essay Skills - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Historical+Enquiry+and+Essay+Skills+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level History - Historical Enquiry and Essay Skills",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level History - Historical Enquiry and Essay Skills",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level History - Historical Enquiry and Essay Skills",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Historical Enquiry and Essay Skills",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/historical-enquiry-and-essay-skills/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Historical Enquiry and Essay Skills",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Historical Enquiry and Essay Skills",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Historical+Enquiry+and+Essay+Skills",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "Geography",
      "topics": [
{
          "title": "Physical Geography",
          "objectives": [
"Explain coastal processes: erosion (hydraulic action, abrasion, attrition, solution), transportation (longshore drift), deposition",
"Describe coastal landforms: erosional (headlands, cliffs, caves, arches, stacks, stumps) and depositional (beaches, spits, bars, tombolos)",
"Understand plate tectonics: plate boundaries (constructive, destructive, conservative, collision), associated hazards (earthquakes, volcanoes, tsunamis)",
"Analyse river processes: erosion (vertical/lateral), transportation (traction, saltation, suspension, solution), deposition",
"Describe river landforms: upper (V-valleys, waterfalls), middle (meanders, oxbow lakes), lower (floodplains, levees, deltas)",
"Explain flooding: causes (physical/human), hydrographs, flood management (hard/soft engineering)"
          ],
          "key": [
"Coastal erosion: hydraulic action (air pressure), abrasion (rock hurling), attrition (rock collision), solution (dissolving)",
"Longshore drift: prevailing wind -> swash angle -> backwash perpendicular -> zigzag transport",
"Landforms: headland (resistant rock), bay (weak rock), cave -> arch -> stack -> stump",
"Plate boundaries: constructive (mid-ocean ridges), destructive (subduction, volcanoes), conservative (transform, earthquakes), collision (fold mountains)",
"River erosion: hydraulic action, abrasion, attrition, solution; vertical (upper), lateral (middle/lower)",
"River landforms: waterfall (hard/soft rock), meander (erosion outer, deposition inner), oxbow (cut-off), levees (deposition floods), delta (deposition at mouth)",
"Flood hydrograph: lag time, peak discharge, rising/falling limb; Management: dams, channel straightening, afforestation, floodplain zoning"
          ],
          "example": "Explain the formation of a waterfall and gorge using geological structure",
          "answer": "River flows over hard rock (cap rock) onto soft rock below. Soft rock erodes faster (hydraulic action, abrasion) creating plunge pool and undercutting. Hard rock collapses -> waterfall retreats upstream -> steep-sided gorge left behind. Cap rock provides resistant layer",
          "practice": [
"Describe formation of a spit",
"Compare constructive vs destructive plate margins",
"Explain factors affecting lag time on hydrograph",
"Evaluate hard vs soft engineering for flood management",
"Annotate a river long profile with processes/landforms"
          ],
          "videos": [
{
              "title": "Physical Geography - Overview",
              "url": "https://www.youtube.com/results?search_query=Physical+Geography+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Physical Geography - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Physical+Geography+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Geography - Physical Geography",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Geography - Physical Geography",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Geography - Physical Geography",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Physical Geography",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/physical-geography/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Physical Geography",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Physical Geography",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Physical+Geography",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Human Geography",
          "objectives": [
"Analyse urbanisation trends: megacities, counterurbanisation, reurbanisation, suburbanisation",
"Understand population change: demographic transition model, population pyramids, migration (push/pull)",
"Evaluate development indicators: HDI, GNI, literacy, life expectancy; inequalities",
"Explain globalisation: flows of capital, labour, goods, ideas; TNCs, supply chains",
"Assess sustainability: ecological footprint, SDGs, resource management"
          ],
          "key": [
"Urbanisation: % urban pop increasing; megacities >10M; counterurbanisation (rich to rural); reurbanisation (gentrification)",
"DTM: Stage 1 (high BR/DR), 2 (falling DR), 3 (falling BR), 4 (low BR/DR), 5 (BR<DR); Pyramids: expanding, stationary, contracting",
"Migration: push (war, poverty, enviro) vs pull (jobs, safety, services); Lee's model",
"Development: HDI (health, education, income); GNI per capita; inequality (Gini, Lorenz)",
"Globalisation: time-space compression; TNCs; global supply chains; winners/losers",
"Sustainability: Brundtland def; ecological footprint; SDGs 17 goals"
          ],
          "example": "Explain how a country's position in the Demographic Transition Model affects its population pyramid shape",
          "answer": "Stage 2 (e.g. Nigeria): high BR, falling DR -> wide base (many young), narrow top (few elderly), pyramidal. Stage 4 (e.g. UK): low BR, low DR -> narrower base, wider top, columnar. Stage 5 (e.g. Japan): BR<DR -> contracting base, bulge at top, inverted pyramid",
          "practice": [
"Compare urbanisation in LIC vs HIC",
"Interpret a population pyramid for Stage 3",
"Explain push/pull factors for rural-urban migration",
"Evaluate HDI vs GNI as development measures",
"Assess impacts of a TNC in a host country"
          ],
          "videos": [
{
              "title": "Human Geography - Overview",
              "url": "https://www.youtube.com/results?search_query=Human+Geography+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Human Geography - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Human+Geography+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Geography - Human Geography",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Geography - Human Geography",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Geography - Human Geography",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Human Geography",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/human-geography/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Human Geography",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Human Geography",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Human+Geography",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Fieldwork and Data Collection",
          "objectives": [
"Design geographical enquiries: hypothesis, aims, risk assessment, ethics",
"Select appropriate sampling: random, systematic, stratified, opportunistic",
"Collect primary data (surveys, measurements, observations) and secondary data (GIS, census, reports)",
"Present data: graphs (bar, line, scatter, choropleth), maps, annotated photos, cross-sections",
"Analyse: statistical tests (Spearman's, chi-squared, Mann-Whitney), qualitative coding",
"Conclude and evaluate: limitations, reliability, validity, improvements"
          ],
          "key": [
"Enquiry: hypothesis (testable), sub-questions, risk assessment, ethical considerations (consent, privacy)",
"Sampling: random (unbiased), systematic (interval), stratified (proportional subgroups), opportunistic (pragmatic)",
"Primary: questionnaires, EQ surveys, sediment analysis, velocity, infiltration; Secondary: OS maps, census, Met Office, academic papers",
"Presentation: proportional circles, choropleth, scatter with trend line, rose diagrams, cross-sections",
"Stats: Spearman's (correlation, ordinal), Chi-squared (categorical association), Mann-Whitney (difference, ordinal)",
"Evaluation: limitations (sample size, bias, equipment), reliability (repeatable), validity (measures what intended)"
          ],
          "example": "Design a hypothesis and sampling strategy to investigate how footpath erosion varies with distance from a car park in a national park",
          "answer": "Hypothesis: Footpath erosion decreases with distance from car park due to visitor pressure decay. Systematic sampling: measure path width, depth, vegetation cover every 50m along 1km transect. Risk: weather, terrain. Ethics: minimise disturbance",
          "practice": [
"Write a hypothesis for river velocity vs distance downstream",
"Choose sampling for urban land use survey",
"Select graph for population vs distance from CBD",
"Explain when to use Spearman's vs Chi-squared",
"Identify limitations of a given fieldwork method"
          ],
          "videos": [
{
              "title": "Fieldwork and Data Collection - Overview",
              "url": "https://www.youtube.com/results?search_query=Fieldwork+and+Data+Collection+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Fieldwork and Data Collection - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Fieldwork+and+Data+Collection+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Geography - Fieldwork and Data Collection",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Geography - Fieldwork and Data Collection",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Geography - Fieldwork and Data Collection",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Fieldwork and Data Collection",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/fieldwork-and-data-collection/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Fieldwork and Data Collection",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Fieldwork and Data Collection",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Fieldwork+and+Data+Collection",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Hazards and Global Issues",
          "objectives": [
"Classify hazards: tectonic (earthquakes, volcanoes, tsunamis), climatic (storms, droughts, heatwaves), geomorphological (landslides)",
"Analyse hazard risk: probability x magnitude x vulnerability; risk equation",
"Explain climate change: evidence (ice cores, temp records), causes (anthropogenic GHG), impacts (sea level, extremes, ecosystems)",
"Evaluate management: prediction, preparation, prevention; adaptation vs mitigation",
"Understand global governance: Paris Agreement, UNFCCC, Sendai Framework, climate justice"
          ],
          "key": [
"Tectonic: plate boundaries; Climatic: atmospheric; Geomorphological: slope failure",
"Risk = Hazard x Vulnerability / Capacity to cope; PAR model (Pressure And Release)",
"Evidence: Keeling curve, IPCC reports, proxy data (ice cores, tree rings); GHG: CO₂, CH₄, N₂O",
"Impacts: sea level rise (thermal expansion, ice melt), extreme weather, biome shifts, ocean acidification",
"Adaptation: adjust to effects (sea walls, drought crops); Mitigation: reduce causes (renewables, reforestation, CCS)",
"Paris 2015: <2 deg C, pursue 1.5 deg C; NDCs; climate finance; Loss and Damage; CBDR (common but differentiated responsibilities)"
          ],
          "example": "Explain why vulnerability is a key component of hazard risk",
          "answer": "Same magnitude earthquake: Haiti 2010 (M7.0, 230k deaths) vs Chile 2010 (M8.8, 500 deaths). Haiti: poor building codes, dense informal housing, weak governance -> high vulnerability. Chile: strict codes, preparedness, wealth -> low vulnerability. Risk depends on vulnerability not just hazard",
          "practice": [
"Classify 2004 Indian Ocean tsunami",
"Explain greenhouse effect mechanism",
"Compare adaptation vs mitigation examples",
"Evaluate Paris Agreement effectiveness",
"Apply PAR model to a case study"
          ],
          "videos": [
{
              "title": "Hazards and Global Issues - Overview",
              "url": "https://www.youtube.com/results?search_query=Hazards+and+Global+Issues+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Hazards and Global Issues - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Hazards+and+Global+Issues+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Geography - Hazards and Global Issues",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Geography - Hazards and Global Issues",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Geography - Hazards and Global Issues",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Hazards and Global Issues",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/hazards-and-global-issues/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Hazards and Global Issues",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Hazards and Global Issues",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Hazards+and+Global+Issues",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "Economics",
      "topics": [
{
          "title": "Microeconomics and Markets",
          "objectives": [
"Analyse demand and supply: shifts vs movements, determinants",
"Determine market equilibrium and disequilibrium (excess demand/supply)",
"Calculate and interpret elasticities: PED, YED, XED, PES",
"Understand consumer and producer surplus, allocative efficiency",
"Evaluate market structures: perfect competition, monopoly, monopolistic competition, oligopoly",
"Analyse labour markets: derived demand, MRP, wage determination, trade unions",
"Evaluate government intervention: max/min prices, taxes, subsidies, regulation"
          ],
          "key": [
"Demand: P↓->Qd↑ (law); Determinants: income, tastes, related goods, expectations, #buyers",
"Supply: P↑->Qs↑; Determinants: input prices, technology, expectations, #sellers, taxes/subsidies",
"Equilibrium: Qd=Qs; Shortage: P<P* -> Qd>Qs; Surplus: P>P* -> Qs>Qd",
"PED = %DeltaQd/%DeltaP; elastic (>1), inelastic (<1), unitary (=1); factors: substitutes, necessity, time, %income",
"YED: normal (>0), inferior (<0); XED: substitutes (>0), complements (<0); PES: time, spare capacity",
"Surplus: CS = area under D above P; PS = area above S below P; Deadweight loss from intervention",
"Market structures: PC (many, homogeneous, free entry); Monopoly (one, barriers); MC (many, differentiated); Oligopoly (few, interdependence)",
"Labour: D = MRP; S = workers; Wage = MRP = MRC in PC; Monopsony: MRC > S; Unions: collective bargaining"
          ],
          "example": "A monopolist faces demand P = 100 - 2Q and has MC = 20. Find profit-maximising output, price, and profit",
          "answer": "MR = 100 - 4Q. Set MR = MC: 100 - 4Q = 20 -> Q = 20. P = 100 - 2(20) = 60. Profit = (P - ATC)Q. ATC = TC/Q. If TC = 20Q + 100, ATC = 20 + 5 = 25. Profit = (60-25)x20 = 700",
          "practice": [
"If PED = -0.5 and price rises 10%, %DeltaQd?",
"Explain why monopolies produce less than PC",
"Calculate CS at P=50, Q=100 for linear demand P=100-Q",
"Evaluate minimum wage using monopsony model",
"Why is PES more elastic in long run?"
          ],
          "videos": [
{
              "title": "Microeconomics and Markets - Overview",
              "url": "https://www.youtube.com/results?search_query=Microeconomics+and+Markets+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Microeconomics and Markets - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Microeconomics+and+Markets+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Economics - Microeconomics and Markets",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Economics - Microeconomics and Markets",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Economics - Microeconomics and Markets",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Microeconomics and Markets",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/microeconomics-and-markets/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Microeconomics and Markets",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Microeconomics and Markets",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Microeconomics+and+Markets",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Macroeconomics",
          "objectives": [
"Measure economic activity: GDP (expenditure, income, output), real vs nominal, GDP deflator",
"Analyse aggregate demand (C+I+G+X-M) and aggregate supply (SRAS, LRAS)",
"Understand inflation: causes (demand-pull, cost-push), costs, CPI/RPI",
"Explain unemployment: types (frictional, structural, cyclical, seasonal), natural rate",
"Evaluate fiscal policy: discretionary vs automatic stabilisers, multiplier, crowding out",
"Evaluate monetary policy: interest rates, QE, transmission mechanism, inflation targeting",
"Analyse exchange rates: determination, appreciation/depreciation effects, BOP",
"Understand supply-side policies: interventionist vs market-based, time lags"
          ],
          "key": [
"GDP = C+I+G+(X-M); Real = nominal/deflatorx100; Deflator = nominal/realx100",
"AD: C (wealth, confidence, rates), I (confidence, rates, tech), G (policy), X-M (exchange rate, world income)",
"SRAS: sticky wages/prices; LRAS: vertical at Yf (classical) or upward (Keynesian); AS shifts: costs, productivity",
"Inflation: demand-pull (AD>AS), cost-push (AS left); CPI basket vs RPI (housing); costs: menu, shoe-leather, uncertainty",
"Unemployment: frictional (search), structural (skills mismatch), cyclical (AD deficient), natural = frictional+structural",
"Fiscal: G↑/T↓ -> AD↑; Multiplier = 1/(1-MPC); Crowding out: G↑->r↑->I↓",
"Monetary: Bank Rate -> market rates -> AD; QE: buy bonds -> money supply↑; Inflation target 2%",
"Exchange rate: floating (market), fixed (peg); Appreciation: X↓ M↑ -> AD↓; BOP: current + capital + financial account"
          ],
          "example": "Using AD/AS, analyse the effect of a rise in oil prices on price level and real output",
          "answer": "Oil price rise -> production costs ↑ -> SRAS shifts left. Result: price level rises (cost-push inflation), real output falls (stagflation). If central bank accommodates (AD↑), output restored but inflation higher. If not, recession",
          "practice": [
"Calculate GDP deflator: nominal=GBP 2.2T, real=GBP 2T",
"Draw AD/AS for recessionary gap",
"Explain multiplier with MPC=0.8",
"Why might fiscal policy be ineffective in open economy?",
"Analyse effect of GBP  depreciation on BOP"
          ],
          "videos": [
{
              "title": "Macroeconomics - Overview",
              "url": "https://www.youtube.com/results?search_query=Macroeconomics+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Macroeconomics - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Macroeconomics+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Economics - Macroeconomics",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Economics - Macroeconomics",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Economics - Macroeconomics",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Macroeconomics",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/macroeconomics/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Macroeconomics",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Macroeconomics",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Macroeconomics",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Market Failure and Government Intervention",
          "objectives": [
"Identify sources of market failure: externalities, public goods, information asymmetry, market power",
"Analyse negative/positive externalities: MSC=MPC+MEC, MSB=MPB+MEB",
"Evaluate policies: Pigouvian taxes, subsidies, tradable permits, regulation, nudges",
"Understand public goods: non-excludable, non-rival; free-rider problem",
"Analyse information asymmetry: adverse selection, moral hazard; solutions",
"Evaluate competition policy: monopolies, mergers, cartels, regulation"
          ],
          "key": [
"Externalities: divergence private/social costs/benefits; Negative: MSC>MPC (pollution); Positive: MSB>MPB (education)",
"Pigouvian tax = MEC at optimum; Subsidy = MEB; Tradable permits: cap-and-trade; Regulation: standards/bans",
"Public goods: non-excludable (can't stop use), non-rival (one's use doesn't reduce other's) -> free rider -> underprovision",
"Info asymmetry: adverse selection (pre-contract, hidden info), moral hazard (post-contract, hidden action); Solutions: signalling, screening, regulation",
"Competition: CMA investigates mergers (SLC test), cartels (price-fixing), abuse of dominance; Regulation: price caps (RPI-X), profit caps"
          ],
          "example": "A factory pollutes a river. MPC = 20+Q, MEC = 5, MPB = 100-Q. Find market output, social optimum, and tax",
          "answer": "Market: MPC=MPB -> 20+Q=100-Q -> Q=40. Social: MSC=MSB -> 20+Q+5=100-Q -> 2Q=75 -> Q=37.5. Tax = MEC = 5 per unit. At Q=37.5, P=100-37.5=62.5. Tax revenue = 5x37.5=187.5",
          "practice": [
"Why is clean air a public good?",
"Draw MSC/MPC for negative externality",
"Explain adverse selection in insurance",
"Evaluate tradable permits vs carbon tax",
"Why regulate natural monopolies?"
          ],
          "videos": [
{
              "title": "Market Failure and Government Intervention - Overview",
              "url": "https://www.youtube.com/results?search_query=Market+Failure+and+Government+Intervention+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Market Failure and Government Intervention - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Market+Failure+and+Government+Intervention+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Economics - Market Failure and Government Intervention",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Economics - Market Failure and Government Intervention",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Economics - Market Failure and Government Intervention",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Market Failure and Government Intervention",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/market-failure-and-government-intervention/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Market Failure and Government Intervention",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Market Failure and Government Intervention",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Market+Failure+and+Government+Intervention",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "International Trade and Development",
          "objectives": [
"Explain absolute and comparative advantage; gains from trade",
"Analyse protectionism: tariffs, quotas, subsidies, VERs; costs/benefits",
"Understand exchange rate systems: fixed, floating, managed; PPP theory",
"Analyse globalisation: drivers, benefits, costs; WTO, trade blocs",
"Evaluate development strategies: import substitution vs export-led, aid, FDI, debt",
"Use development indicators: HDI, MDGs/SDGs, inequality (Gini, Lorenz)"
          ],
          "key": [
"Absolute: produce more with same resources; Comparative: lower opportunity cost -> specialise -> trade",
"Tariff: tax on imports -> domestic P↑, Qd↓, Qs↑, govt revenue, DWL; Quota: quantity limit; Subsidy: domestic producers",
"Floating: market; Fixed: central bank intervention; Managed: dirty float; PPP: identical goods same price in common currency",
"Globalisation: trade↑, capital flows↑, migration↑, tech diffusion; WTO: rules, disputes; Blocs: EU, USMCA, ASEAN",
"Development: import substitution (protect infant industries) vs export-led (E Asian tigers); Aid: tied/untied; Debt: HIPC initiative",
"HDI: life expectancy, education (mean/expected yrs), GNI pc; Gini: 0=perfect equality, 1=perfect inequality; Lorenz curve"
          ],
          "example": "Country A: 10 labour hours for 1 cloth or 5 wine. Country B: 6 cloth or 4 wine. Who has comparative advantage in what?",
          "answer": "A: OC 1 cloth = 2 wine (10/5), 1 wine = 0.5 cloth. B: OC 1 cloth = 0.67 wine (6/4), 1 wine = 1.5 cloth. B has CA in cloth (lower OC), A has CA in wine. A exports wine, B exports cloth. Both gain",
          "practice": [
"Calculate opportunity costs for CA",
"Draw tariff diagram showing DWL",
"Explain J-curve effect",
"Evaluate export-led vs import substitution",
"Interpret Lorenz curve and Gini"
          ],
          "videos": [
{
              "title": "International Trade and Development - Overview",
              "url": "https://www.youtube.com/results?search_query=International+Trade+and+Development+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "International Trade and Development - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=International+Trade+and+Development+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Economics - International Trade and Development",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Economics - International Trade and Development",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Economics - International Trade and Development",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - International Trade and Development",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/international-trade-and-development/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - International Trade and Development",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - International Trade and Development",
              "url": "https://www.bbc.co.uk/bitesize/search?q=International+Trade+and+Development",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "Business Studies",
      "topics": [
{
          "title": "Marketing",
          "objectives": [
"Analyse market segmentation: geographic, demographic, psychographic, behavioural",
"Apply the marketing mix (7 Ps): Product, Price, Place, Promotion, People, Process, Physical evidence",
"Evaluate pricing strategies: penetration, skimming, psychological, competitive, cost-plus, dynamic",
"Understand product life cycle and extension strategies",
"Analyse promotion: above/below the line, digital marketing, promotional mix",
"Evaluate place/distribution channels: direct, indirect, omnichannel"
          ],
          "key": [
"Segmentation: geo (location), demo (age, gender, income), psycho (lifestyle, values), behavioural (usage, loyalty)",
"7 Ps: Product (features, quality, branding), Price (strategies), Place (channels), Promotion (mix), People (service), Process (delivery), Physical evidence (tangibles)",
"Pricing: penetration (low, gain share), skimming (high, early adopters), psychological (GBP 9.99), competitive (match), cost-plus (markup), dynamic (real-time)",
"PLC: introduction, growth, maturity, decline; Extension: new markets, new uses, repositioning",
"Promotion: ATL (TV, radio), BTL (direct, PR, sales promotion), Digital (SEO, PPC, social, email)",
"Distribution: direct (manufacturer->consumer), indirect (wholesaler/retailer), omnichannel (integrated)"
          ],
          "example": "A new energy drink targets 18-25 males. Propose segmentation, pricing, and promotion strategy",
          "answer": "Segmentation: demographic (18-25, male), psychographic (active, risk-takers), behavioural (gym-goers). Pricing: penetration (GBP 1.50) to gain share quickly. Promotion: social media influencers, gym sponsorships, sampling at events. Place: gyms, convenience stores, online subscription",
          "practice": [
"Segment the electric car market",
"Compare penetration vs skimming for new iPhone",
"Design promotional mix for local bakery",
"Evaluate omnichannel for fashion retailer",
"Apply PLC to DVD players"
          ],
          "videos": [
{
              "title": "Marketing - Overview",
              "url": "https://www.youtube.com/results?search_query=Marketing+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Marketing - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Marketing+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Business Studies - Marketing",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Business Studies - Marketing",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Business Studies - Marketing",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Marketing",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/marketing/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Marketing",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Marketing",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Marketing",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Finance and Accounts",
          "objectives": [
"Interpret financial statements: income statement, balance sheet, cash flow statement",
"Calculate and interpret profitability, liquidity, efficiency, gearing ratios",
"Analyse break-even: contribution, margin of safety, target profit",
"Understand sources of finance: internal (retained profit) vs external (debt, equity)",
"Evaluate investment appraisal: payback, ARR, NPV, IRR",
"Understand budgets: purpose, types (zero-based, incremental), variance analysis"
          ],
          "key": [
"Income statement: revenue, COGS, gross profit, expenses, operating profit, profit for year",
"Balance sheet: non-current assets, current assets, current liabilities, non-current liabilities, equity",
"Cash flow: operating, investing, financing; free cash flow",
"Ratios: Gross/Net margin, ROCE, Current/Acid test, Inventory/Payables/Receivables days, Gearing (debt/equity)",
"Break-even: FC / (P - VC); Margin of safety = actual - BE; Target profit = (FC + target) / contribution",
"Finance: internal (retained profit, asset sale); external: debt (loans, bonds, overdraft), equity (shares, venture capital)",
"Investment: Payback (time), ARR (avg profit/avg investment), NPV (discounted CF), IRR (discount rate for NPV=0)",
"Budgets: plan, coordinate, control; Zero-based (justify all), Incremental (last year +/-); Variance: adverse/favourable"
          ],
          "example": "FC=GBP 50,000, VC=GBP 5/unit, P=GBP 15. Find break-even, margin of safety at 12,000 units, units for GBP 30,000 profit",
          "answer": "Contribution = 15-5=10. BE = 50,000/10 = 5,000 units. MoS = 12,000 - 5,000 = 7,000 units (58%). Target: (50,000+30,000)/10 = 8,000 units",
          "practice": [
"Calculate gross/net margin from income statement",
"Interpret current ratio 1.5 vs 0.8",
"NPV: GBP 100k initial, GBP 30k/yr 5yrs, 10% discount",
"Compare debt vs equity finance",
"Calculate adverse variance: budget GBP 20k, actual GBP 25k"
          ],
          "videos": [
{
              "title": "Finance and Accounts - Overview",
              "url": "https://www.youtube.com/results?search_query=Finance+and+Accounts+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Finance and Accounts - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Finance+and+Accounts+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Business Studies - Finance and Accounts",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Business Studies - Finance and Accounts",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Business Studies - Finance and Accounts",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Finance and Accounts",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/finance-and-accounts/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Finance and Accounts",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Finance and Accounts",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Finance+and+Accounts",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Operations Management",
          "objectives": [
"Compare production methods: job, batch, flow, cell, mass customisation",
"Evaluate quality management: QC vs QA, TQM, Kaizen, Six Sigma, benchmarking",
"Analyse capacity utilisation, efficiency, productivity",
"Understand lean production: JIT, Kanban, waste reduction (Muda), 5S",
"Analyse supply chain: procurement, logistics, outsourcing, supplier relationships",
"Evaluate technology impact: automation, AI, IoT, Industry 4.0"
          ],
          "key": [
"Job: one-off, high skill, high cost; Batch: groups, flexible; Flow: continuous, high volume, low variety; Cell: U-shape, multi-skilled; Mass custom: flow + flexibility",
"QC (inspection) vs QA (prevention); TQM: culture, continuous improvement; Kaizen: small incremental; Six Sigma: DMAIC, 3.4 defects/million; Benchmarking: best practice",
"Capacity utilisation = actual/max x100%; Efficiency = standard hours/actual hours; Productivity = output/input",
"Lean: eliminate Muda (overproduction, waiting, transport, over-processing, inventory, motion, defects); JIT: pull system; Kanban: visual signal; 5S: Sort, Set, Shine, Standardise, Sustain",
"Supply chain: procurement (supplier selection), logistics (transport, warehousing), outsourcing (core vs non-core), supplier development",
"Industry 4.0: cyber-physical systems, IoT, big data, AI, additive manufacturing, digital twins"
          ],
          "example": "A furniture maker switches from batch to flow production. Analyse implications for cost, quality, flexibility",
          "answer": "Cost: lower unit cost (economies of scale, less setup), but high capital investment. Quality: more consistent (standardised), but defects affect large volumes. Flexibility: reduced (dedicated line), harder to customise. Workforce: deskilling, potential redundancy. Inventory: lower WIP with JIT",
          "practice": [
"Compare job vs flow for bespoke vs standard products",
"Explain DMAIC in Six Sigma",
"Calculate capacity utilisation: actual 800, max 1000",
"List 7 wastes (Muda) with examples",
"Evaluate outsourcing IT support"
          ],
          "videos": [
{
              "title": "Operations Management - Overview",
              "url": "https://www.youtube.com/results?search_query=Operations+Management+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Operations Management - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Operations+Management+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Business Studies - Operations Management",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Business Studies - Operations Management",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Business Studies - Operations Management",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Operations Management",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/operations-management/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Operations Management",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Operations Management",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Operations+Management",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "People and Leadership",
          "objectives": [
"Evaluate motivation theories: Taylor, Mayo, Maslow, Herzberg, McClelland, Vroom, Adams",
"Analyse leadership styles: autocratic, democratic, laissez-faire, situational (Hersey-Blanchard), transformational",
"Understand organisational structures: tall/flat, centralised/decentralised, matrix, network",
"Evaluate recruitment/selection: job analysis, person spec, methods (interviews, tests, assessment centres)",
"Understand training/development: on/off job, induction, CPD, appraisal (360 deg , MBO)",
"Analyse employee relations: trade unions, collective bargaining, industrial action, ACAS"
          ],
          "key": [
"Content theories: Maslow (hierarchy), Herzberg (hygiene/motivators), McClelland (need achiev/affil/power); Process: Vroom (expectancy), Adams (equity)",
"Styles: Autocratic (decides alone), Democratic (consults), Laissez-faire (delegates); Situational: telling/selling/participating/delegating; Transformational: inspire, intellectually stimulate",
"Tall: many layers, narrow span; Flat: few layers, wide span; Centralised: top decides; Decentralised: delegated; Matrix: dual reporting",
"Recruitment: job description, person spec; Internal vs external; Selection: CV, interview (structured/unstructured), psychometric, assessment centre",
"Training: on-job (shadowing, coaching), off-job (courses, e-learning); Appraisal: 360 deg  (multi-source), MBO (objectives)",
"Unions: represent workers, collective bargaining, industrial action (strike, work-to-rule); ACAS: conciliation, arbitration, advisory"
          ],
          "example": "Apply Herzberg to a call centre with high turnover. Propose changes",
          "answer": "Hygiene factors: pay, conditions, supervision, policy -> ensure competitive pay, ergonomic chairs, supportive managers, fair policies. Motivators: achievement, recognition, responsibility, growth -> team targets with bonuses, employee of month, job enrichment (team leader roles), career path to management",
          "practice": [
"Compare Maslow vs Herzberg",
"Apply Vroom expectancy to sales commission",
"Evaluate transformational leadership in crisis",
"Design selection process for graduate scheme",
"Analyse pros/cons of matrix structure"
          ],
          "videos": [
{
              "title": "People and Leadership - Overview",
              "url": "https://www.youtube.com/results?search_query=People+and+Leadership+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "People and Leadership - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=People+and+Leadership+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Business Studies - People and Leadership",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Business Studies - People and Leadership",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Business Studies - People and Leadership",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - People and Leadership",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/people-and-leadership/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - People and Leadership",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - People and Leadership",
              "url": "https://www.bbc.co.uk/bitesize/search?q=People+and+Leadership",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Strategy and the External Environment",
          "objectives": [
"Apply strategic analysis: SWOT, PESTEL, Porter's Five Forces, Core Competences, Boston Matrix",
"Evaluate strategic direction: Ansoff Matrix (market penetration, development, product development, diversification)",
"Analyse competitive strategy: Porter's Generic (cost leadership, differentiation, focus)",
"Evaluate growth methods: organic (internal) vs inorganic (M&A, alliances, franchising)",
"Understand strategic implementation: resource allocation, change management (Kotter, Lewin), KPIs",
"Analyse business ethics and CSR: Carroll's pyramid, stakeholders vs shareholders"
          ],
          "key": [
"SWOT: internal S/W, external O/T; PESTEL: Political, Economic, Social, Technological, Environmental, Legal",
"Porter 5 Forces: rivalry, new entrants, substitutes, buyer power, supplier power",
"Core competences: valuable, rare, inimitable, non-substitutable (VRIN)",
"Boston Matrix: Stars (high share, high growth), Cash Cows (high share, low growth), Question Marks (low share, high growth), Dogs (low share, low growth)",
"Ansoff: existing/new products x existing/new markets -> 4 strategies",
"Porter Generic: Cost leadership (lowest cost), Differentiation (unique value), Focus (niche)",
"Organic: internal investment; Inorganic: M&A (horizontal, vertical, conglomerate), strategic alliances, joint ventures, franchising",
"Change: Kotter 8 steps (urgency, coalition, vision, communicate, empower, wins, consolidate, anchor); Lewin: unfreeze, change, refreeze",
"CSR: Carroll (economic, legal, ethical, philanthropic); Stakeholder theory vs shareholder primacy; Triple bottom line (people, planet, profit)"
          ],
          "example": "Use Porter's Five Forces to analyse the UK supermarket industry",
          "answer": "Rivalry: high (Tesco, Sainsbury, Asda, Morrisons, Aldi, Lidl -- price wars). New entrants: low (high capital, established supply chains, brand loyalty). Substitutes: medium (convenience stores, online, markets). Buyer power: high (price-sensitive, low switching cost, loyalty cards). Supplier power: medium (large buyers, but branded goods have power). Overall: low profitability",
          "practice": [
"Apply PESTEL to electric vehicle industry",
"Place Apple products in Boston Matrix",
"Compare cost leadership vs differentiation for Ryanair vs BA",
"Evaluate M&A vs organic growth for tech startup",
"Apply Kotter to digital transformation"
          ],
          "videos": [
{
              "title": "Strategy and the External Environment - Overview",
              "url": "https://www.youtube.com/results?search_query=Strategy+and+the+External+Environment+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Strategy and the External Environment - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Strategy+and+the+External+Environment+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Business Studies - Strategy and the External Environment",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Business Studies - Strategy and the External Environment",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Business Studies - Strategy and the External Environment",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Strategy and the External Environment",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/strategy-and-the-external-environment/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Strategy and the External Environment",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Strategy and the External Environment",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Strategy+and+the+External+Environment",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "Computer Science",
      "topics": [
{
          "title": "Programming Fundamentals",
          "objectives": [
"Use variables, constants, and data types (integer, real, boolean, character, string)",
"Implement control structures: sequence, selection (if/else, switch), iteration (for, while, do-while)",
"Design and use functions/procedures: parameters (value/reference), return values, scope",
"Handle input/output: file I/O, exceptions, validation",
"Apply string manipulation: concatenation, slicing, searching, formatting",
"Use random number generation and libraries"
          ],
          "key": [
"Data types: int, float, bool, char, string; type casting; constants vs variables",
"Selection: if/elif/else, switch/case (match in Python 3.10+); nested conditions",
"Iteration: for (definite), while (indefinite), do-while (at least once); break/continue",
"Functions: definition, call, parameters (positional, keyword, default), return, recursion",
"Scope: local, global, nonlocal; shadowing; modules and imports",
"String: len, index, slice, split, join, replace, format, f-strings, regex basics",
"File: open/close, read/write modes, with statement, try/except/else/finally"
          ],
          "example": "Write a function that reads a file of integers and returns the median",
          "answer": "def median_from_file(filename):\n    with open(filename) as f:\n        nums = sorted(int(line.strip()) for line in f if line.strip())\n    n = len(nums)\n    if n == 0: return None\n    mid = n // 2\n    return nums[mid] if n % 2 else (nums[mid-1] + nums[mid]) / 2",
          "practice": [
"Write a program that validates email format using regex",
"Implement a recursive factorial function",
"Create a menu-driven calculator with functions",
"Write a function to count word frequencies in a text file",
"Handle division by zero with try/except"
          ],
          "videos": [
{
              "title": "Programming Fundamentals - Overview",
              "url": "https://www.youtube.com/results?search_query=Programming+Fundamentals+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Programming Fundamentals - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Programming+Fundamentals+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Computer Science - Programming Fundamentals",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Computer Science - Programming Fundamentals",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Computer Science - Programming Fundamentals",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Programming Fundamentals",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/programming-fundamentals/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Programming Fundamentals",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Programming Fundamentals",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Programming+Fundamentals",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Data Structures and Algorithms",
          "objectives": [
"Implement and use arrays, lists, stacks, queues, linked lists, trees, graphs, hash tables",
"Analyse time and space complexity using Big-O notation",
"Implement and trace search algorithms: linear, binary, hash-based",
"Implement and trace sorting algorithms: bubble, insertion, merge, quick, heap",
"Understand recursion and divide-and-conquer; apply to tree/graph traversals",
"Apply algorithms to problems: shortest path (Dijkstra), MST (Prim/Kruskal), topological sort"
          ],
          "key": [
"Arrays: contiguous, O(1) access; Lists: dynamic, O(1) append amortised; Stacks: LIFO, push/pop; Queues: FIFO, enqueue/dequeue",
"Linked lists: singly/doubly, O(1) insert/delete at known position, O(n) access",
"Trees: binary, BST (left<root<right), AVL/Red-Black (balanced); traversals: pre/in/post-order, level-order",
"Graphs: adjacency matrix/list; directed/undirected, weighted/unweighted; BFS/DFS",
"Hash tables: O(1) average, collisions (chaining, open addressing), load factor",
"Big-O: O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2ⁿ); best/average/worst case",
"Search: linear O(n), binary O(log n) sorted, hash O(1); Sort: bubble/insertion O(n^2), merge/quick/heap O(n log n)",
"Recursion: base case, recursive case; Tree traversals; Graph: Dijkstra (shortest path), Prim/Kruskal (MST), Topological sort (DAG)"
          ],
          "example": "Trace quicksort on [3, 6, 8, 10, 1, 2, 1] with pivot as first element",
          "answer": "Pivot=3. Partition: [1,2,1] + [3] + [6,8,10]. Recurse left: pivot=1 -> [1] + [1] + [2]. Right: pivot=6 -> [] + [6] + [8,10] -> pivot=8 -> [] + [8] + [10]. Result: [1,1,2,3,6,8,10]",
          "practice": [
"Implement stack using list",
"Write binary search recursive",
"Trace merge sort on [38,27,43,3,9,82,10]",
"Implement BFS for shortest path in unweighted graph",
"Design hash function for string keys"
          ],
          "videos": [
{
              "title": "Data Structures and Algorithms - Overview",
              "url": "https://www.youtube.com/results?search_query=Data+Structures+and+Algorithms+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Data Structures and Algorithms - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Data+Structures+and+Algorithms+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Computer Science - Data Structures and Algorithms",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Computer Science - Data Structures and Algorithms",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Computer Science - Data Structures and Algorithms",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Data Structures and Algorithms",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/data-structures-and-algorithms/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Data Structures and Algorithms",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Data Structures and Algorithms",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Data+Structures+and+Algorithms",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Computer Systems and Architecture",
          "objectives": [
"Explain CPU architecture: ALU, CU, registers (PC, ACC, MAR, MDR, CIR, SR)",
"Describe fetch-decode-execute cycle and pipelining",
"Understand memory hierarchy: registers, cache (L1/L2/L3), RAM, virtual memory, secondary storage",
"Compare CISC vs RISC, parallel processing (SIMD, MIMD, multicore)",
"Understand instruction sets: addressing modes, instruction formats, assembly basics",
"Analyse performance: clock speed, CPI, IPC, Amdahl's law"
          ],
          "key": [
"CPU: ALU (arithmetic/logic), CU (control signals), Registers: PC (next instruction), ACC (results), MAR (address), MDR (data), CIR (instruction), SR (flags)",
"FDE: Fetch (PC to MAR, memory to MDR/CIR, PC++), Decode (CU interprets CIR), Execute (ALU/control)",
"Pipelining: fetch/decode/execute overlap; hazards (data, control, structural)",
"Memory: Registers > L1 cache > L2 > L3 > RAM > SSD > HDD; Virtual memory: paging, page table, TLB, page fault",
"CISC: complex instructions, variable length, microcode; RISC: simple, fixed length, load/store, more registers",
"Parallel: SIMD (single instruction, multiple data), MIMD (multicore); Amdahl: speedup = 1/((1-p) + p/n)"
          ],
          "example": "A program has 20 percent serial code. Max speedup on 4 cores?",
          "answer": "Amdahl: speedup = 1/((1-0.8) + 0.8/4) = 1/(0.2 + 0.2) = 2.5x. Even infinite cores: 1/0.2 = 5x",
          "practice": [
"List registers and their purposes",
"Draw FDE cycle diagram",
"Explain cache hit/miss",
"Compare CISC vs RISC",
"Calculate speedup: 30 percent serial, 8 cores"
          ],
          "videos": [
{
              "title": "Computer Systems and Architecture - Overview",
              "url": "https://www.youtube.com/results?search_query=Computer+Systems+and+Architecture+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Computer Systems and Architecture - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Computer+Systems+and+Architecture+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Computer Science - Computer Systems and Architecture",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Computer Science - Computer Systems and Architecture",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Computer Science - Computer Systems and Architecture",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Computer Systems and Architecture",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/computer-systems-and-architecture/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Computer Systems and Architecture",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Computer Systems and Architecture",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Computer+Systems+and+Architecture",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Networks and Internet",
          "objectives": [
"Compare network topologies: star, mesh, bus, ring, hybrid",
"Understand TCP/IP stack: Application, Transport, Internet, Link layers",
"Analyse key protocols: HTTP/HTTPS, DNS, TCP, UDP, IP, DHCP, FTP, SSH",
"Understand IP addressing: IPv4 (classes, subnetting, CIDR), IPv6",
"Describe cybersecurity threats: malware, phishing, DoS, MITM, SQL injection, XSS",
"Apply security: encryption (symmetric/asymmetric, TLS/SSL), firewalls, VPNs, authentication"
          ],
          "key": [
"Topologies: Star (central hub), Mesh (all connected), Bus (shared cable), Ring (token passing)",
"TCP/IP: App (HTTP, DNS, FTP), Transport (TCP reliable, UDP fast), Internet (IP routing), Link (Ethernet, WiFi)",
"TCP: 3-way handshake, sequencing, flow control, congestion control; UDP: connectionless, low latency",
"DNS: hierarchical (root, TLD, authoritative); recursive/iterative queries; records (A, AAAA, MX, CNAME)",
"IPv4: 32-bit, dotted decimal, classes A/B/C, subnet mask, CIDR (/24); IPv6: 128-bit, hex, no NAT needed",
"Threats: malware (virus, worm, ransomware), phishing, DoS/DDoS, MITM, SQLi (input sanitisation), XSS (output encoding)",
"Encryption: Symmetric (AES, same key), Asymmetric (RSA, public/private); TLS: handshake, certificates, CA; Firewall: packet filter, stateful, application; VPN: encrypted tunnel; Auth: MFA, OAuth, JWT"
          ],
          "example": "Explain the TLS handshake process",
          "answer": "1. Client hello (supported ciphers). 2. Server hello (chosen cipher) + certificate (public key, CA signed). 3. Client verifies cert (CA trusted, not expired, domain matches). 4. Client generates pre-master secret, encrypts with server public key, sends. 5. Both derive session keys. 6. Encrypted communication begins",
          "practice": [
"Subnet 192.168.1.0/24 into 4 subnets",
"Compare TCP vs UDP for video streaming",
"Explain DNS resolution steps",
"Describe SQL injection prevention",
"How does RSA key exchange work?"
          ],
          "videos": [
{
              "title": "Networks and Internet - Overview",
              "url": "https://www.youtube.com/results?search_query=Networks+and+Internet+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Networks and Internet - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Networks+and+Internet+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Computer Science - Networks and Internet",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Computer Science - Networks and Internet",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Computer Science - Networks and Internet",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Networks and Internet",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/networks-and-internet/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Networks and Internet",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Networks and Internet",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Networks+and+Internet",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Boolean Logic and Relational Databases",
          "objectives": [
"Construct and simplify Boolean expressions using laws (De Morgan, distribution, absorption)",
"Design combinational logic circuits: adders, multiplexers, decoders",
"Understand sequential logic: flip-flops (SR, D, JK), registers, counters",
"Design relational databases: ER modelling, normalisation (1NF, 2NF, 3NF, BCNF)",
"Write SQL: DDL (CREATE, ALTER), DML (SELECT, INSERT, UPDATE, DELETE), joins, aggregation",
"Understand ACID properties, transactions, concurrency control, indexing"
          ],
          "key": [
"Boolean laws: Identity, Null, Idempotent, Complement, Commutative, Associative, Distributive, De Morgan, Absorption",
"K-maps: 2-4 variables, groups of 1s (SOP) or 0s (POS); don't cares",
"Circuits: Half adder (XOR+AND), Full adder (2 half + OR), MUX (select), Decoder (binary->one-hot)",
"Flip-flops: SR (set/reset), D (data), JK (toggle); Registers: shift, storage; Counters: async/sync",
"ER: entities, attributes, relationships (1:1, 1:N, M:N), keys (PK, FK, CK)",
"Normalisation: 1NF (atomic), 2NF (no partial FD), 3NF (no transitive FD), BCNF (det⇒cand key)",
"SQL: SELECT...FROM...WHERE...GROUP BY...HAVING...ORDER BY; JOINs (INNER, LEFT, RIGHT, FULL)",
"Aggregation: COUNT, SUM, AVG, MIN, MAX; Subqueries; ACID: Atomicity, Consistency, Isolation, Durability",
"Concurrency: locks (shared/exclusive), deadlock, 2PL; Indexes: B-tree, hash; Query optimisation"
          ],
          "example": "Normalise to 3NF: Student(StudentID, Name, CourseID, CourseName, TutorID, TutorName)",
          "answer": "FDs: StudentID->Name, CourseID->CourseName, TutorID, TutorID->TutorName. 1NF: atomic. 2NF: remove partial FD (CourseID->CourseName). Course(CourseID, CourseName, TutorID), Tutor(TutorID, TutorName), Student(StudentID, Name, CourseID). 3NF: remove transitive FD (TutorID->TutorName). Already in 3NF",
          "practice": [
"Simplify: A·(A+B) + A·B",
"Design full adder from half adders",
"Draw ER for library system",
"Write SQL: students with avg grade > 70",
"Explain ACID with examples"
          ],
          "videos": [
{
              "title": "Boolean Logic and Relational Databases - Overview",
              "url": "https://www.youtube.com/results?search_query=Boolean+Logic+and+Relational+Databases+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Boolean Logic and Relational Databases - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Boolean+Logic+and+Relational+Databases+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Computer Science - Boolean Logic and Relational Databases",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Computer Science - Boolean Logic and Relational Databases",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Computer Science - Boolean Logic and Relational Databases",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Boolean Logic and Relational Databases",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/boolean-logic-and-relational-databases/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Boolean Logic and Relational Databases",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Boolean Logic and Relational Databases",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Boolean+Logic+and+Relational+Databases",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    },
{
      "name": "Psychology",
      "topics": [
{
          "title": "Approaches and Perspectives",
          "objectives": [
"Compare and evaluate the major psychological approaches: biological, cognitive, behaviourist, psychodynamic, humanistic",
"Understand the biological approach: genetics, neurochemistry, brain structure, evolution",
"Evaluate the cognitive approach: schema, information processing, cognitive neuroscience",
"Analyse behaviourism: classical conditioning, operant conditioning, social learning theory",
"Understand the psychodynamic approach: unconscious, psychosexual stages, defence mechanisms",
"Evaluate the humanistic approach: self-actualisation, free will, congruence, conditions of worth"
          ],
          "key": [
"Biological: genes, neurotransmitters (dopamine, serotonin), brain localisation, evolution, twin/adoption studies",
"Cognitive: schema, mental models, computer analogy, cognitive neuroscience (fMRI, PET)",
"Behaviourist: Pavlov (classical: NS->CS), Skinner (operant: reinforcement/punishment), Bandura (SLT: observation, modelling)",
"Psychodynamic: Freud (id/ego/superego, psychosexual stages, defence mechanisms), unconscious motivation",
"Humanistic: Maslow (hierarchy), Rogers (self-concept, congruence, unconditional positive regard), free will",
"Debates: Nature vs nurture, determinism vs free will, reductionism vs holism, nomothetic vs idiographic"
          ],
          "example": "Explain how the biological and cognitive approaches differ in explaining depression",
          "answer": "Biological: genetic predisposition, serotonin/noradrenaline deficit, hippocampal atrophy -> treatment: SSRIs, ECT. Cognitive: Beck's negative triad (self, world, future), cognitive distortions, schema -> treatment: CBT (challenge thoughts). Biological = reductionist, medical; Cognitive = mental processes, empowerment",
          "practice": [
"Compare SLT vs operant conditioning",
"Evaluate twin studies for nature/nurture",
"Explain Freud's defence mechanisms with examples",
"Apply Maslow to workplace motivation",
"Evaluate cognitive neuroscience as reductionist"
          ],
          "videos": [
{
              "title": "Approaches and Perspectives - Overview",
              "url": "https://www.youtube.com/results?search_query=Approaches+and+Perspectives+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Approaches and Perspectives - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Approaches+and+Perspectives+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Psychology - Approaches and Perspectives",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Psychology - Approaches and Perspectives",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Psychology - Approaches and Perspectives",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Approaches and Perspectives",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/approaches-and-perspectives/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Approaches and Perspectives",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Approaches and Perspectives",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Approaches+and+Perspectives",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Research Methods",
          "objectives": [
"Design experiments: lab, field, natural, quasi; IV, DV, controls, counterbalancing, randomisation",
"Understand sampling: random, stratified, systematic, opportunity, volunteer; generalisability",
"Analyse data: descriptive (mean, median, mode, SD, range), inferential (parametric/non-parametric tests)",
"Understand ethics: BPS guidelines, informed consent, deception, debrief, right to withdraw, confidentiality",
"Evaluate reliability (test-retest, inter-rater) and validity (internal, external, ecological, construct)",
"Write psychological reports: abstract, intro, method, results, discussion, references (APA)"
          ],
          "key": [
"Experimental designs: independent measures, repeated measures, matched pairs; controls: standardisation, counterbalancing, random allocation",
"Sampling: random (unbiased), stratified (proportional subgroups), systematic (interval), opportunity (convenience), volunteer (self-select)",
"Descriptive: mean (parametric), median (skewed), mode (nominal), SD (spread), range; Inferential: t-test, Mann-Whitney, Wilcoxon, Chi-squared, Spearman, Pearson",
"Ethics: consent, deception (cost-benefit), debrief, withdrawal, confidentiality, protection from harm; BPS code",
"Reliability: consistency (test-retest, inter-rater, split-half); Validity: internal (IV->DV), external (generalisable), ecological (real-life), construct (measures concept)",
"Report structure: Abstract (150w), Intro (lit review, hypothesis), Method (design, sample, materials, procedure), Results (stats, tables), Discussion (interpret, eval, implications), Refs (APA)"
          ],
          "example": "Design an experiment to test if caffeine improves reaction time. Identify IV, DV, design, controls, sampling, ethics",
          "answer": "IV: caffeine (200mg vs placebo). DV: reaction time (ms) on computer task. Design: repeated measures (counterbalanced). Controls: same time of day, same task, blind. Sampling: volunteer students (opportunity). Ethics: consent, right to withdraw, debrief, medical screening for caffeine sensitivity",
          "practice": [
"Choose test: compare 2 independent groups, ordinal data",
"Explain counterbalancing",
"When to use Spearman vs Pearson",
"Evaluate opportunity sampling",
"Write APA reference for journal article"
          ],
          "videos": [
{
              "title": "Research Methods - Overview",
              "url": "https://www.youtube.com/results?search_query=Research+Methods+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Research Methods - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Research+Methods+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Psychology - Research Methods",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Psychology - Research Methods",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Psychology - Research Methods",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Research Methods",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/research-methods/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Research Methods",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Research Methods",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Research+Methods",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Memory and Cognitive Psychology",
          "objectives": [
"Explain and evaluate the Multi-Store Model (Atkinson-Shiffrin): sensory, STM, LTM",
"Understand Working Memory Model (Baddeley-Hitch): central executive, phonological loop, visuospatial sketchpad, episodic buffer",
"Explain LTM types: episodic, semantic, procedural; encoding, storage, retrieval",
"Analyse forgetting: interference (proactive/retroactive), retrieval failure, decay, motivated forgetting",
"Evaluate eyewitness testimony: misleading information, anxiety, cognitive interview",
"Understand cognitive development: Piaget (stages), Vygotsky (ZPD, scaffolding)"
          ],
          "key": [
"MSM: Sensory (iconic/echoic, <1s) -> attention -> STM (acoustic, 7+/-2, 18-30s) -> rehearsal -> LTM (semantic, unlimited); WMM: CE (attention), PL (speech), VSSP (visual), EB (integration); LTM: episodic (events), semantic (facts), procedural (skills)",
"Encoding: acoustic (STM), semantic (LTM); Storage: consolidation; Retrieval: recall, recognition, relearning",
"Forgetting: Proactive (old->new), Retroactive (new->old), Retrieval failure (cue-dependent), Decay (trace fades), Motivated (repression)",
"EWT: Loftus & Palmer (leading questions), anxiety (weapon focus), Cognitive interview (context reinstatement, report everything, reverse order, change perspective)",
"Piaget: sensorimotor, preoperational, concrete, formal; schemas, assimilation, accommodation; Vygotsky: ZPD, scaffolding, social interaction"
          ],
          "example": "Explain how the Working Memory Model accounts for dual-task performance better than the Multi-Store Model",
          "answer": "MSM: single STM store -> two verbal tasks interfere. WMM: separate stores (PL for verbal, VSSP for visual) -> can do verbal + visual simultaneously. Evidence: Baddeley (verbal reasoning + tracking). PL overload impairs both if both verbal",
          "practice": [
"Compare MSM vs WMM",
"Explain retrieval failure with example",
"Evaluate cognitive interview",
"Apply Piaget to conservation task",
"Evaluate Loftus & Palmer methodology"
          ],
          "videos": [
{
              "title": "Memory and Cognitive Psychology - Overview",
              "url": "https://www.youtube.com/results?search_query=Memory+and+Cognitive+Psychology+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Memory and Cognitive Psychology - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Memory+and+Cognitive+Psychology+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Psychology - Memory and Cognitive Psychology",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Psychology - Memory and Cognitive Psychology",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Psychology - Memory and Cognitive Psychology",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Memory and Cognitive Psychology",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/memory-and-cognitive-psychology/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Memory and Cognitive Psychology",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Memory and Cognitive Psychology",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Memory+and+Cognitive+Psychology",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Social Influence and Attachment",
          "objectives": [
"Explain conformity: types (compliance, identification, internalisation), Asch, Zimbardo",
"Explain obedience: Milgram, situational vs dispositional factors, agency theory",
"Understand resistance to social influence: social support, locus of control",
"Explain minority influence: Moscovici, consistency, commitment, flexibility",
"Understand attachment: Bowlby (monotropy, critical period, internal working model), Ainsworth (Strange Situation, types)",
"Evaluate cultural variations in attachment, Romanian orphan studies, institutionalisation"
          ],
          "key": [
"Conformity: Compliance (public only), Identification (group membership), Internalisation (true belief); Asch (line length, 32% conform), Zimbardo (Stanford prison)",
"Obedience: Milgram (65% to 450V), agency theory (agentic/autonomous state), legitimacy of authority, gradual commitment",
"Resistance: social support (ally), locus of control (internal resist); Minority influence: consistency, commitment, flexibility, snowball effect",
"Attachment: Bowlby (evolutionary, monotropy, critical period 0-2.5yrs, IWM), Ainsworth: Secure (B), Insecure-avoidant (A), Insecure-resistant (C); Disorganised (D)",
"Cultural: van IJzendoorn (meta-analysis, secure universal but variations), Romanian orphans (Rutter, ERA study, privation effects)",
"Influence on later relationships: IWM -> parenting, peer, romantic (Hazan & Shaver)"
          ],
          "example": "Explain why Milgram's participants obeyed using agency theory",
          "answer": "Agentic state: individual sees self as agent of authority, not responsible. Autonomous state: self-directed. Shift triggered by: legitimate authority, institutional context, gradual commitment (15V steps), buffers (victim not visible). Dispositional: authoritarian personality (Adorno)",
          "practice": [
"Distinguish compliance vs internalisation",
"Evaluate Zimbardo ethics",
"Explain internal working model",
"Compare attachment types in Strange Situation",
"Evaluate Romanian orphan study"
          ],
          "videos": [
{
              "title": "Social Influence and Attachment - Overview",
              "url": "https://www.youtube.com/results?search_query=Social+Influence+and+Attachment+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Social Influence and Attachment - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Social+Influence+and+Attachment+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Psychology - Social Influence and Attachment",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Psychology - Social Influence and Attachment",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Psychology - Social Influence and Attachment",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Social Influence and Attachment",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/social-influence-and-attachment/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Social Influence and Attachment",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Social Influence and Attachment",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Social+Influence+and+Attachment",
              "description": "BBC Bitesize revision resources"
            }
          ]
        },
{
          "title": "Psychopathology",
          "objectives": [
"Define abnormality: statistical infrequency, deviation from social norms, failure to function adequately, deviation from ideal mental health",
"Understand phobias: behavioural (classical conditioning, two-process), cognitive (irrational thoughts), biological (preparedness)",
"Explain depression: biological (genetics, neurotransmitters, neuroendocrine), cognitive (Beck's triad, learned helplessness), psychological treatments",
"Understand OCD: biological (genetics, basal ganglia, serotonin), cognitive (intrusive thoughts, inflated responsibility), treatments",
"Evaluate treatments: biological (SSRIs, benzodiazepines, ECT), psychological (CBT, exposure, systematic desensitisation)",
"Understand diagnosis and classification: DSM-5, ICD-11, reliability/validity issues, comorbidity, cultural bias"
          ],
          "key": [
"Definitions: Statistical (rare, e.g. IQ<70), Social norms (culture-specific), FFAD (distress, dysfunction), Ideal MH (Jahoda: autonomy, reality perception, etc.)",
"Phobias: Two-process (classical: fear acquisition, operant: avoidance maintenance); Preparedness (Seligman: evolved fears); CBT: exposure, cognitive restructuring",
"Depression: Biological (5-HTT gene, serotonin, cortisol/HPA axis); Cognitive (Beck: negative triad, schema, cognitive distortions); Learned helplessness (Seligman); Treatments: SSRIs (6-8 weeks), CBT (behavioural activation, cognitive restructuring)",
"OCD: Obsessions (intrusive), Compulsions (repetitive); Biological (COMT, SLC1A1, basal ganglia, serotonin); Cognitive (inflated responsibility, thought-action fusion); ERP (exposure response prevention)",
"Treatments: SSRIs (fluoxetine), Benzos (short-term), ECT (severe, resistant); CBT (gold standard for anxiety/depression); ERP (OCD)",
"Classification: DSM-5 (APA), ICD-11 (WHO); Reliability (inter-rater), Validity (construct, predictive); Comorbidity (e.g. depression+anxiety); Culture-bound syndromes"
          ],
          "example": "Explain the two-process model of phobias and evaluate it",
          "answer": "Classical: neutral stimulus (spider) paired with fear (trauma) -> CS elicits CR (fear). Operant: avoidance reduces fear -> negative reinforcement maintains phobia. Evaluation: explains acquisition/maintenance; ignores cognition (irrational thoughts), preparedness (why spiders not flowers?), individual differences; CBT addresses limitations",
          "practice": [
"Compare four definitions of abnormality",
"Explain Beck's negative triad",
"Evaluate SSRIs for depression",
"Describe ERP for OCD",
"Discuss cultural bias in DSM-5"
          ],
          "videos": [
{
              "title": "Psychopathology - Overview",
              "url": "https://www.youtube.com/results?search_query=Psychopathology+A-Level",
              "source": "YouTube Search"
            },
{
              "title": "Psychopathology - Exam Questions",
              "url": "https://www.youtube.com/results?search_query=Psychopathology+exam+questions",
              "source": "YouTube Search"
            }
          ],
          "past_papers": [
{
              "title": "AQA A-Level Psychology - Psychopathology",
              "url": "https://www.aqa.org.uk/find-past-papers-and-mark-schemes",
              "board": "AQA"
            },
{
              "title": "Edexcel A-Level Psychology - Psychopathology",
              "url": "https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html",
              "board": "Edexcel"
            },
{
              "title": "OCR A-Level Psychology - Psychopathology",
              "url": "https://www.ocr.org.uk/qualifications/past-paper-finder/",
              "board": "OCR"
            }
          ],
          "external_links": [
{
              "title": "Physics & Maths Tutor - Psychopathology",
              "url": "https://www.physicsandmathstutor.com/maths-revision/a-level-edexcel/pure-maths/psychopathology/",
              "description": "Free notes, worksheets, and past paper questions by topic"
            },
{
              "title": "Dr Frost Maths - Psychopathology",
              "url": "https://drfrostmaths.com/",
              "description": "Free resources, slides, and interactive questions"
            },
{
              "title": "BBC Bitesize - Psychopathology",
              "url": "https://www.bbc.co.uk/bitesize/search?q=Psychopathology",
              "description": "BBC Bitesize revision resources"
            }
          ]
        }
      ]
    }
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
        t = re.sub(r'\s*[--]\s*(Revision|Lessons)?\s*Notes?\s*$', '', t).strip()
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
  }
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
        '<div class="affiliate-card-title">Fastmail -- Private Email</div>'
        '<div class="affiliate-card-desc">Privacy-first email with no ads and no tracking</div>'
        '<div class="affiliate-card-store">fastmail.com</div></a>',
        '<a href="https://www.dynadot.com/?ref=scottrix" class="affiliate-card" target="_blank" rel="nofollow noopener">'
        '<div class="affiliate-card-title">Dynadot -- Domain Registration -></div>'
        '<div class="affiliate-card-desc">Register or transfer domains with free SSL and affordable pricing</div>'
        '<div class="affiliate-card-store">dynadot.com</div></a>',
        '<a href="https://zen.mention-me.com/m/ol/yv3qsjix-scott-harrison" class="affiliate-card" target="_blank" rel="nofollow noopener">'
        '<div class="affiliate-card-title">Zen Internet -- UK Broadband -></div>'
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

    # Board differences removed from topic pages -- they live on subject landing pages
    diffs_html = ""

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

    # Video Resources section
    video_section = ""
    videos = topic.get("videos", [])
    if videos:
        video_items = "".join(f'<li><a href="{esc(v["url"])}" target="_blank" rel="noopener">{esc(v["title"])}</a> -- {esc(v["source"])}</li>' for v in videos)
        video_section = f"""<section class="section">
<h2>🎬 Video Resources</h2>
<ul>{video_items}</ul>
</section>"""

    # Past Papers & Exam Resources section
    pastpapers_section = ""
    pastpapers = topic.get("past_papers", [])
    if pastpapers:
        pp_items = "".join(f'<li><a href="{esc(p["url"])}" target="_blank" rel="noopener">{esc(p["title"])}</a> -- {esc(p["board"])}</li>' for p in pastpapers)
        pastpapers_section = f"""<section class="section">
<h2>📄 Past Papers & Exam Resources</h2>
<ul>{pp_items}</ul>
</section>"""

    # Additional Reading & External Links section
    external_section = ""
    externals = topic.get("external_links", [])
    if externals:
        ext_items = "".join(f'<li><a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["title"])}</a> -- {esc(e["description"])}</li>' for e in externals)
        external_section = f"""<section class="section">
<h2>🔗 Further Reading & Resources</h2>
<ul>{ext_items}</ul>
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
    twitter_desc = f"{esc(title)} -- A-Level {esc(subject_name)} revision notes."

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
<div class="disclaimer-banner"><strong>A-Level {mode} Aid:</strong> This resource is designed to support your revision and may contain errors. If you find a discrepancy with your class teaching, your teacher is correct -- please let us know at <a href="mailto:alevelrevise@scott.scottrix.co.uk">alevelrevise@scott.scottrix.co.uk</a>.</div>

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
<a class="fastmail-topbar" data-banner="dynadot" href="https://www.dynadot.com/?ref=scottrix" target="_blank" rel="nofollow noopener" hidden><img src="{link_root}dynadot-banner.jpg" alt="Dynadot -- register a new domain, web hosting, SSL" loading="lazy" onerror="this.parentElement.style.display='none';document.querySelector('[data-banner=fastmail]').hidden=false"></a>
<script>(function(){{var fm=document.querySelector('[data-banner=fastmail]');var dd=document.querySelector('[data-banner=dynadot]');if(Math.random()<0.5){{fm.hidden=true;dd.hidden=false}}}})();</script>

{keypoints_section}
{objectives_section}
{diffs_html}
{example_section}
{practice_section}
{video_section}
{pastpapers_section}
{external_section}
{lesson_section}

<nav class="topic-nav">
<a href="{link_root}{sslug}.html">← Back to {esc(subject_name)} Overview</a>
<a href="{link_root}index.html">All Subjects -></a>
</nav>
</main>
<footer class="site-footer">
<p>A-Level {mode} - Free revision notes for all subjects and exam boards</p>
<p>Content for educational purposes only. Always cross-reference with official specifications.</p>
<p>This site contains affiliate links. We may earn a commission if you purchase through these links.</p>
<p>(c) 2025 | <a href="https://github.com/scottrix/{site}">GitHub</a> | <a href="{link_root}privacy.html">Privacy Policy</a> | <a href="mailto:alevelrevise@scott.scottrix.co.uk">Contact</a></p>
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
