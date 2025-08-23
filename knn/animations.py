from manim import *
import numpy as np

# ---------- 1) DISTANCE IN 1D ----------
class Distance1D(Scene):
    def construct(self):
        title = Text("Distance in 1D: |a - b|").to_edge(UP)
        self.play(FadeIn(title))

        # Number line
        nl = NumberLine(
            x_range=[0, 6, 1],
            length=10,
            include_numbers=True,
            include_tip=True
        ).shift(DOWN*0.5)
        self.play(Create(nl))

        # Points A, B, C (small distances)
        A_x, B_x, C_x = 1.0, 1.7, 2.4   # |A-B|=0.7, |A-C|=1.4
        A = Dot(nl.n2p(A_x), color=YELLOW)
        B = Dot(nl.n2p(B_x), color=BLUE)
        C = Dot(nl.n2p(C_x), color=RED)

        # Spread labels further apart
        LABEL_SPREAD = 1
        A_lbl = MathTex(f"A={A_x:.1f}").next_to(A, UP, buff=0.25).shift(LEFT*LABEL_SPREAD + UP*0.1)
        B_lbl = MathTex(f"B={B_x:.1f}").next_to(B, UP, buff=0.35)  # a touch higher
        C_lbl = MathTex(f"C={C_x:.1f}").next_to(C, UP, buff=0.25).shift(RIGHT*LABEL_SPREAD + UP*0.1)

        self.play(FadeIn(A, A_lbl), FadeIn(B, B_lbl), FadeIn(C, C_lbl))

        # Distances (both visible simultaneously)
        d_AB = abs(A_x - B_x)
        d_AC = abs(A_x - C_x)

        seg_AB = Line(nl.n2p(A_x), nl.n2p(B_x), color=BLUE)
        seg_AC = Line(nl.n2p(A_x), nl.n2p(C_x), color=RED)

        # Brace offsets (AB higher ~2x)
        OFFSET_UP_AB = 0.70   # twice the previous 0.35
        OFFSET_DOWN_AC = 0.35

        brace_AB = BraceBetweenPoints(nl.n2p(A_x), nl.n2p(B_x), direction=UP)
        brace_AB.shift(UP * OFFSET_UP_AB)
        lab_AB = brace_AB.get_tex(rf"|A-B|={d_AB:.1f}")
        lab_AB.next_to(brace_AB, UP, buff=0.05)

        brace_AC = BraceBetweenPoints(nl.n2p(A_x), nl.n2p(C_x), direction=DOWN)
        brace_AC.shift(DOWN * OFFSET_DOWN_AC)
        lab_AC = brace_AC.get_tex(rf"|A-C|={d_AC:.1f}")
        lab_AC.next_to(brace_AC, DOWN, buff=0.05)

        self.play(
            Create(seg_AB), Create(seg_AC),
            Create(brace_AB), Create(brace_AC),
            FadeIn(lab_AB), FadeIn(lab_AC),
        )

        compare = MathTex(r"|A-B|<|A-C|").next_to(title, DOWN)
        self.play(FadeIn(compare))

        formula = MathTex(r"d(a,b)=|a-b|").to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1.0)

# ---------- 2) DISTANCE IN 2D ----------
class Distance2D(Scene):
    def construct(self):
        title = Text("Distance in 2D: Euclidean").to_edge(UP)  # same text size
        self.play(FadeIn(title))

        # Build geometry first (no text yet)
        ax = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_tip": True},
        ).to_edge(LEFT, buff=0.25)

        P = np.array([0.5, 2, 0])
        Q = np.array([4, 6, 0])
        Pdot = Dot(ax.c2p(*P[:2]), color=YELLOW)
        Qdot = Dot(ax.c2p(*Q[:2]), color=RED)

        PxQy = np.array([Q[0], P[1], 0])  # (4,2)
        leg_x = DashedLine(ax.c2p(*P[:2]),   ax.c2p(*PxQy[:2]), color=BLUE)
        leg_y = DashedLine(ax.c2p(*PxQy[:2]), ax.c2p(*Q[:2]),   color=BLUE)
        hypo  = Line(ax.c2p(*P[:2]), ax.c2p(*Q[:2]), color=GREEN)

        brace_dx = BraceBetweenPoints(ax.c2p(*P[:2]),   ax.c2p(*PxQy[:2]))
        brace_dy = BraceBetweenPoints(ax.c2p(*PxQy[:2]), ax.c2p(*Q[:2]))

        graph = VGroup(ax, Pdot, Qdot, leg_x, leg_y, hypo, brace_dx, brace_dy)

        self.play(Create(ax))
        self.play(FadeIn(Pdot, Qdot))
        self.play(Create(leg_x), Create(leg_y), Create(hypo))
        self.play(Create(brace_dx), Create(brace_dy))

        # --- Make the graph smaller, keep text unscaled ---
        GRAPH_SCALE = 0.5          # smaller graph; tweak to taste
        GROUP_SHIFT = LEFT*(-0.25) + DOWN*0.15  # optional reposition
        self.play(graph.animate.scale(GRAPH_SCALE).shift(GROUP_SHIFT))

        # Now add text (unchanged size), positioned relative to the *scaled* geometry
        axis_labels = ax.get_axis_labels(MathTex("x"), MathTex("y"))
        self.play(FadeIn(axis_labels))

        # Point labels: push P more left/down; Q a bit right/up
        Plbl = MathTex("P(1,2)").next_to(Pdot, DOWN+LEFT, buff=0.55)
        Qlbl = MathTex("Q(4,6)").next_to(Qdot, UP+RIGHT,  buff=0.35)

        # Brace labels created AFTER scaling so they sit correctly
        dx_label = brace_dx.get_tex(r"\Delta x = |4-1|=3").shift(RIGHT*0.5)
        dy_label = brace_dy.get_tex(r"\Delta y = |6-2|=4")

        self.play(FadeIn(Plbl, Qlbl, dx_label, dy_label))

        # Formula bottom-right (same text size)
        formula = MathTex(
            r"d(P,Q)=\sqrt{(\Delta x)^2+(\Delta y)^2}=\sqrt{3^2+4^2}=5"
        ).to_corner(DR).shift(RIGHT*0.1 + DOWN*0.1)
        self.play(Write(formula))
        self.wait(1.0)

# ---------- 3) DISTANCE IN 3D ----------
class Distance3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65*DEGREES, theta=-45*DEGREES)

        title = Text("Distance in 3D: Euclidean").to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title))

        ax = ThreeDAxes(x_range=[0, 5, 1], y_range=[0, 5, 1], z_range=[0, 5, 1])
        self.play(Create(ax))

        # Points
        P = np.array([1.0, 1.0, 1.0])
        Q = np.array([3.0, 2.0, 4.0])
        Pdot = Dot3D(ax.c2p(*P), color=YELLOW, radius=0.06)
        Qdot = Dot3D(ax.c2p(*Q), color=RED,    radius=0.06)
        self.play(FadeIn(Pdot), FadeIn(Qdot))

        # Axis-aligned legs
        P1 = np.array([Q[0], P[1], P[2]])
        P2 = np.array([Q[0], Q[1], P[2]])
        leg1 = DashedLine(ax.c2p(*P),  ax.c2p(*P1), color=BLUE)
        leg2 = DashedLine(ax.c2p(*P1), ax.c2p(*P2), color=BLUE)
        leg3 = DashedLine(ax.c2p(*P2), ax.c2p(*Q),  color=BLUE)
        self.play(Create(leg1), Create(leg2), Create(leg3))

        # Diagonal
        diag = Line(ax.c2p(*P), ax.c2p(*Q), color=GREEN)
        self.play(Create(diag))

        # >>> Scale/shift the graph (axes + geometry) <<<
        GRAPH_SCALE = 0.25                 # smaller graph (try 0.7, 0.6, etc.)
        # GRAPH_SHIFT = LEFT*1.2 + DOWN*(4)  # optional: reposition
        graph = VGroup(ax, Pdot, Qdot, leg1, leg2, leg3, diag).shift(RIGHT*4.5 + DOWN*3).scale(GRAPH_SCALE)
        # self.play(graph.animate.scale(GRAPH_SCALE).shift(GRAPH_SHIFT))

        # Formula (fixed to screen; stays same size)
        dx, dy, dz = Q - P
        formula = MathTex(
            r"d(P,Q)=\sqrt{(\Delta x)^2+(\Delta y)^2+(\Delta z)^2}",
            r"=\sqrt{%.0f^2+%.0f^2+%.0f^2}=%.2f" % (dx, dy, dz, np.sqrt(dx*dx+dy*dy+dz*dz))
        ).scale(0.9).to_corner(UR).shift(DOWN*6)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))

        # Camera move
        # self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)

# ---------- 4) CURSE OF DIMENSIONALITY ----------
from manim import *
import numpy as np

class CurseOfDimensionality(ThreeDScene):
    def construct(self):
        # Title - smaller and cleaner
        title = Text("Curse of Dimensionality", font_size=36).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title))

        r = 1.0  # Reduced radius for better fit

        # ---------- 1D: interval [-r, r] ----------
        line = NumberLine(x_range=[-1.5, 1.5, 0.5], length=4, include_numbers=False)
        seg = Line(line.n2p(-r), line.n2p(r), color=YELLOW, stroke_width=6)
        
        # Simpler labeling
        lab1 = MathTex(r"V_1(r) = 2r", font_size=28)
        cap1 = Text("1D", font_size=24, color=YELLOW)
        
        g1_labels = VGroup(cap1, lab1).arrange(DOWN, buff=0.1)
        g1_labels.next_to(line, DOWN, buff=0.3)
        
        g1 = VGroup(line, seg, g1_labels)
        g1.to_edge(LEFT, buff=1.5).shift(UP * 1.5)

        self.play(Create(line), Create(seg), FadeIn(g1_labels))

        # ---------- 2D: disk ----------
        ax2 = Axes(
            x_range=[-1.5, 1.5, 0.5], 
            y_range=[-1.5, 1.5, 0.5], 
            x_length=3, 
            y_length=3,
            axis_config={"stroke_width": 1, "stroke_opacity": 0.3}
        )
        circ = Circle(radius=ax2.x_axis.n2p(r)[0] - ax2.x_axis.n2p(0)[0], color=BLUE, fill_opacity=0.3)
        circ.move_to(ax2.c2p(0, 0))
        
        lab2 = MathTex(r"V_2(r) = \pi r^2", font_size=28)
        cap2 = Text("2D", font_size=24, color=BLUE)
        
        g2_labels = VGroup(cap2, lab2).arrange(DOWN, buff=0.1)
        g2_labels.next_to(ax2, DOWN, buff=0.3)
        
        g2 = VGroup(ax2, circ, g2_labels)
        g2.move_to(ORIGIN + UP * 1.5)

        self.play(Create(ax2), Create(circ), FadeIn(g2_labels))

        # ---------- 3D: sphere ----------
        ax3 = ThreeDAxes(
            x_range=[-1.5, 1.5, 0.5], 
            y_range=[-1.5, 1.5, 0.5], 
            z_range=[-1.5, 1.5, 0.5],
            x_length=3,
            y_length=3,
            z_length=3,
            axis_config={"stroke_width": 1, "stroke_opacity": 0.3}
        )
        sphere = Sphere(center=ORIGIN, radius=r)
        sphere.move_to(ax3.c2p(0, 0, 0))
        sphere.set_fill(RED, opacity=0.4).set_stroke(RED, width=1)

        lab3 = MathTex(r"V_3(r) = \frac{4}{3}\pi r^3", font_size=28)
        cap3 = Text("3D", font_size=24, color=RED)
        
        g3_labels = VGroup(cap3, lab3).arrange(DOWN, buff=0.1)
        g3_labels.next_to(ax3, DOWN, buff=0.3)
        
        g3 = VGroup(ax3, sphere, g3_labels)
        g3.to_edge(RIGHT, buff=1.5).shift(UP * 1.5)

        # Set camera orientation for better 3D view
        self.set_camera_orientation(phi=65*DEGREES, theta=-30*DEGREES)
        self.play(Create(ax3), FadeIn(sphere), FadeIn(g3_labels))

        self.wait(0.5)

        # ---------- Key insights - moved left ----------
        insights = VGroup(
            MathTex(r"\text{General: } V_d(r) \propto r^d", font_size=32),
            Text("Higher dimensions makes exponentially larger neighborhoods", font_size=20),
            Text("Data becomes increasingly sparse in high-dimensional spaces", font_size=20)
        ).arrange(DOWN, buff=0.3)
        
        insights.to_edge(DOWN, buff=0.8).shift(LEFT * 2.5)
        self.add_fixed_in_frame_mobjects(insights)
        self.play(Write(insights[0]))
        self.play(FadeIn(insights[1:]))

        # ---------- Numerical example - moved left ----------
        example = VGroup(
            Text("Example ratios (ball volume / cube volume):", font_size=18),
            MathTex(
                r"1D: 1.00 \quad 2D: 0.785 \quad 3D: 0.524 \quad 10D: 0.002",
                font_size=20
            )
        ).arrange(DOWN, buff=0.15)
        
        example.next_to(insights, UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(example)
        self.play(FadeIn(example))

        self.wait(2)

# ---------- 5) MINKOWSKI BALLS IN 2D ----------
class MinkowskiBalls2D(Scene):
    def construct(self):
        title = Text("Neighborhood shape depends on the metric (p-norm)").scale(0.8).to_edge(UP)
        self.play(FadeIn(title))

        ax = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=6, y_length=6,
            axis_config={"include_tip": True}
        )
        self.play(Create(ax))

        r = 1.5

        # L2: circle (blue)
        circle = Circle(radius=ax.x_axis.n2p(r)[0]-ax.x_axis.n2p(0)[0], color=BLUE).move_to(ax.c2p(0,0))
        # Create labels group for centering
        l2_lbl = MathTex(r"p=2\;(\text{Euclidean})", color=BLUE).scale(0.6)
        l1_lbl = MathTex(r"p=1\;(\text{Manhattan})", color=YELLOW).scale(0.6)
        linf_lbl = MathTex(r"p=\infty\;(\text{Chebyshev})", color=RED).scale(0.6)
        
        # Arrange labels horizontally
        labels_group = VGroup(l2_lbl, l1_lbl, linf_lbl).arrange(RIGHT, buff=1).next_to(ax, DOWN)
        
        self.play(Create(circle), FadeIn(l2_lbl))
        self.wait(0.6)

        # L1: diamond |x|+|y|=r (yellow)
        # Build polygon for |x|+|y|=r
        pts = [ax.c2p( r,  0),
               ax.c2p( 0,  r),
               ax.c2p(-r,  0),
               ax.c2p( 0, -r)]
        diamond = Polygon(*pts, color=YELLOW)
        self.play(Create(diamond), FadeIn(l1_lbl))
        self.wait(0.6)

        # L∞: square max(|x|,|y|)=r (red)
        square = Square(side_length=2*(ax.x_axis.n2p(r)[0]-ax.x_axis.n2p(0)[0]), color=RED).move_to(ax.c2p(0,0))
        self.play(Create(square), FadeIn(linf_lbl))
        self.wait(1.2)

        takeaway = Text("Change the metric → change the neighbors → change the decision.", slant=ITALIC).scale(0.5).to_edge(DOWN)
        self.play(Write(takeaway))
        self.wait(1.5)
        
# ---------- 6) THUMBNAIL ---------- 
class KNNVisualization(Scene):
    def construct(self):
        title = Text("K-Nearest Neighbors Algorithm").scale(0.8).to_edge(UP)
        self.play(FadeIn(title))
        
        # Create axes
        ax = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 5, 1],
            x_length=7, y_length=5,
            axis_config={"include_tip": False, "include_numbers": False}
        )
        self.play(Create(ax))
        
        # Training data points
        # Class A (blue circles)
        class_a_points = [
            ax.c2p(1, 1), ax.c2p(2, 1.5), ax.c2p(1.5, 2.5),
            ax.c2p(0.5, 3), ax.c2p(2.5, 3.5)
        ]
        
        # Class B (red squares)
        class_b_points = [
            ax.c2p(4, 1), ax.c2p(5, 1.5), ax.c2p(4.5, 2),
            ax.c2p(5.5, 2.5), ax.c2p(4, 3.5)
        ]
        
        # Create class A points (blue circles)
        class_a_dots = VGroup(*[
            Circle(radius=0.1, color=BLUE, fill_opacity=1).move_to(point)
            for point in class_a_points
        ])
        
        # Create class B points (red squares)
        class_b_dots = VGroup(*[
            Square(side_length=0.2, color=RED, fill_opacity=1).move_to(point)
            for point in class_b_points
        ])
        
        # Legend
        legend_a = VGroup(
            Circle(radius=0.1, color=BLUE, fill_opacity=1),
            Text("Class A", color=BLUE).scale(0.5)
        ).arrange(RIGHT, buff=0.2).to_corner(UR, buff=0.5)
        
        legend_b = VGroup(
            Square(side_length=0.2, color=RED, fill_opacity=1),
            Text("Class B", color=RED).scale(0.5)
        ).arrange(RIGHT, buff=0.2).next_to(legend_a, DOWN, buff=0.2)
        
        self.play(
            Create(class_a_dots),
            Create(class_b_dots),
            FadeIn(legend_a),
            FadeIn(legend_b)
        )
        self.wait(1)
        
        # New point to classify (green star)
        new_point_pos = ax.c2p(3, 2.5)
        new_point = RegularPolygon(n=5, radius=0.15, color=GREEN, fill_opacity=1).move_to(new_point_pos)
        new_point_label = Text("New Point", color=GREEN).scale(0.4).next_to(new_point, UP, buff=0.1)
        
        self.play(Create(new_point), FadeIn(new_point_label))
        self.wait(0.5)
        
        # Show k=3 circle
        k_value = Text("k = 3").scale(0.6).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(k_value))
        
        # Calculate distances and find 3 nearest neighbors
        # For visualization, we'll manually select 3 closest points
        nearest_points = [
            (ax.c2p(2.5, 3.5), BLUE),  # Class A
            (ax.c2p(4, 3.5), RED),     # Class B  
            (ax.c2p(4.5, 2), RED)      # Class B
        ]
        
        # Draw distance lines to k nearest neighbors
        distance_lines = VGroup()
        for point_pos, color in nearest_points:
            line = DashedLine(new_point_pos, point_pos, color=GRAY)
            distance_lines.add(line)
        
        self.play(Create(distance_lines))
        self.wait(1)
        
        # Highlight the k nearest neighbors
        highlights = VGroup()
        for point_pos, color in nearest_points:
            highlight = Circle(radius=0.25, color=YELLOW, stroke_width=4).move_to(point_pos)
            highlights.add(highlight)
        
        self.play(Create(highlights))
        self.wait(1)
        
        # Show voting result
        voting_text = Text("Voting: 1 × Class A, 2 × Class B").scale(0.5).next_to(k_value, UP, buff=0.3)
        result_text = Text("Prediction: Class B", color=RED).scale(0.6).next_to(voting_text, UP, buff=0.3)
        
        self.play(FadeIn(voting_text))
        self.wait(0.5)
        self.play(FadeIn(result_text))
        
        # Change new point color to predicted class
        self.play(new_point.animate.set_color(RED))
        self.wait(2)