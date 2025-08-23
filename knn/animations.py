# knn_distances.py
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

        # Points A, B, C
        A_x, B_x, C_x = 1.0, 2.5, 5.0
        A = Dot(nl.n2p(A_x), color=YELLOW)
        B = Dot(nl.n2p(B_x), color=BLUE)
        C = Dot(nl.n2p(C_x), color=RED)
        A_lbl = MathTex("A=1.0").next_to(A, UP)
        B_lbl = MathTex("B=2.5").next_to(B, UP)
        C_lbl = MathTex("C=5.0").next_to(C, UP)
        self.play(FadeIn(A, A_lbl), FadeIn(B, B_lbl), FadeIn(C, C_lbl))

        # |A-B|
        seg_AB = Line(nl.n2p(A_x), nl.n2p(B_x), color=BLUE)
        brace_AB = BraceBetweenPoints(nl.n2p(A_x), nl.n2p(B_x))
        lab_AB = brace_AB.get_tex(r"|A-B|=1.5")
        self.play(Create(seg_AB), GrowFromCenter(brace_AB), FadeIn(lab_AB))
        self.wait(0.7)
        self.play(FadeOut(seg_AB), FadeOut(brace_AB), FadeOut(lab_AB))

        # |A-C|
        seg_AC = Line(nl.n2p(A_x), nl.n2p(C_x), color=RED)
        brace_AC = BraceBetweenPoints(nl.n2p(A_x), nl.n2p(C_x))
        lab_AC = brace_AC.get_tex(r"|A-C|=4.0")
        self.play(Create(seg_AC), GrowFromCenter(brace_AC), FadeIn(lab_AC))
        self.wait(1.0)

        # Formula callout
        formula = MathTex(r"d(a,b)=|a-b|").to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1.5)


# ---------- 2) DISTANCE IN 2D ----------
class Distance2D(Scene):
    def construct(self):
        title = Text("Distance in 2D: Euclidean").to_edge(UP)
        self.play(FadeIn(title))

        # Axes
        ax = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": True},
        ).to_edge(LEFT, buff=0.5)
        labels = ax.get_axis_labels(MathTex("x"), MathTex("y"))
        self.play(Create(ax), FadeIn(labels))

        # Points
        P = np.array([1, 2, 0])
        Q = np.array([4, 6, 0])
        Pdot = Dot(ax.c2p(*P[:2]), color=YELLOW)
        Qdot = Dot(ax.c2p(*Q[:2]), color=RED)
        Plbl = MathTex("P(1,2)").next_to(Pdot, DOWN+LEFT*0.5)
        Qlbl = MathTex("Q(4,6)").next_to(Qdot, UP+RIGHT*0.2)
        self.play(FadeIn(Pdot, Qdot, Plbl, Qlbl))

        # Legs dx, dy
        PxQy = np.array([Q[0], P[1], 0])   # (4,2)
        leg_x = DashedLine(ax.c2p(*P[:2]), ax.c2p(*PxQy[:2]), color=BLUE)
        leg_y = DashedLine(ax.c2p(*PxQy[:2]), ax.c2p(*Q[:2]), color=BLUE)
        self.play(Create(leg_x), Create(leg_y))

        # Hypotenuse
        hypo = Line(ax.c2p(*P[:2]), ax.c2p(*Q[:2]), color=GREEN)
        self.play(Create(hypo))

        # Braces and labels
        brace_dx = BraceBetweenPoints(ax.c2p(*P[:2]), ax.c2p(*PxQy[:2]))
        brace_dy = BraceBetweenPoints(ax.c2p(*PxQy[:2]), ax.c2p(*Q[:2]))
        dx_label = brace_dx.get_tex(r"\Delta x = |4-1|=3")
        dy_label = brace_dy.get_tex(r"\Delta y = |6-2|=4")
        self.play(GrowFromCenter(brace_dx), FadeIn(dx_label))
        self.play(GrowFromCenter(brace_dy), FadeIn(dy_label))

        # Formula
        formula = MathTex(
            r"d(P,Q)=\sqrt{(\Delta x)^2+(\Delta y)^2}=\sqrt{3^2+4^2}=5"
        ).to_edge(RIGHT).shift(UP*0.5)
        self.play(Write(formula))
        self.wait(1.5)


# ---------- 3) DISTANCE IN 3D ----------
class Distance3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65*DEGREES, theta=-45*DEGREES)

        title = Text("Distance in 3D: Euclidean").to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title))

        ax = ThreeDAxes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            z_range=[0, 5, 1]
        )
        self.play(Create(ax))

        # Points
        P = np.array([1.0, 1.0, 1.0])
        Q = np.array([3.0, 2.0, 4.0])

        Pdot = Dot3D(ax.c2p(*P), color=YELLOW, radius=0.06)
        Qdot = Dot3D(ax.c2p(*Q), color=RED, radius=0.06)
        self.play(FadeIn(Pdot), FadeIn(Qdot))

        # Axis-aligned "box" path: P -> (Qx,Py,Pz) -> (Qx,Qy,Pz) -> Q
        P1 = np.array([Q[0], P[1], P[2]])
        P2 = np.array([Q[0], Q[1], P[2]])

        leg1 = DashedLine(ax.c2p(*P),  ax.c2p(*P1), color=BLUE)
        leg2 = DashedLine(ax.c2p(*P1), ax.c2p(*P2), color=BLUE)
        leg3 = DashedLine(ax.c2p(*P2), ax.c2p(*Q),  color=BLUE)
        self.play(Create(leg1), Create(leg2), Create(leg3))

        # Diagonal (true Euclidean distance)
        diag = Line(ax.c2p(*P), ax.c2p(*Q), color=GREEN)
        self.play(Create(diag))

        # Formula fixed to screen
        dx, dy, dz = Q - P
        formula = MathTex(
            r"d(P,Q)=\sqrt{(\Delta x)^2+(\Delta y)^2+(\Delta z)^2}",
            r"=\sqrt{%.0f^2+%.0f^2+%.0f^2}=%.2f" % (dx, dy, dz, np.sqrt(dx*dx+dy*dy+dz*dz))
        ).scale(0.9)
        formula.to_corner(UR)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))

        # Slow camera move for depth
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)


# ---------- 4) CURSE OF DIMENSIONALITY ----------
class CurseOfDimensionality(Scene):
    def construct(self):
        title = Text("Neighborhood size grows ~ r^d (curse of dimensionality)").scale(0.9).to_edge(UP)
        self.play(FadeIn(title))

        r = 1.2

        # 1D: interval [-r, r]
        line = NumberLine(x_range=[-1.6, 1.6, 0.4], length=8, include_numbers=False)
        seg = Line(line.n2p(-r), line.n2p(r), color=YELLOW)
        br = BraceBetweenPoints(line.n2p(-r), line.n2p(r))
        lab = br.get_tex(r"\text{length }=2r")
        cap1 = VGroup(Text("1D 'ball' (interval)").scale(0.5), MathTex(r"V_1(r)=2r")).arrange(DOWN, buff=0.25)
        cap1.next_to(line, DOWN)
        g1 = VGroup(line, seg, br, lab, cap1).to_edge(LEFT, buff=0.6).shift(UP*0.5)
        self.play(Create(line), Create(seg), GrowFromCenter(br), FadeIn(lab))
        self.play(FadeIn(cap1))

        # 2D: circle area = pi r^2
        ax2 = Axes(x_range=[-1.6, 1.6, 0.8], y_range=[-1.6, 1.6, 0.8], x_length=3.2, y_length=3.2)
        circ = Circle(radius=ax2.x_axis.n2p(r)[0]-ax2.x_axis.n2p(0)[0], color=BLUE).move_to(ax2.c2p(0,0))
        cap2 = VGroup(Text("2D ball (disk)").scale(0.5), MathTex(r"V_2(r)=\pi r^2")).arrange(DOWN, buff=0.25)
        cap2.next_to(ax2, DOWN)
        g2 = VGroup(ax2, circ, cap2).move_to(ORIGIN+UP*0.5)
        self.play(Create(ax2), Create(circ), FadeIn(cap2))

        # 3D: sphere volume = 4/3 pi r^3 (draw cross-section + label)
        ax3 = Axes(x_range=[-1.6, 1.6, 0.8], y_range=[-1.6, 1.6, 0.8], x_length=3.2, y_length=3.2)
        sphere_outline = Circle(radius=ax3.x_axis.n2p(r)[0]-ax3.x_axis.n2p(0)[0], color=RED).move_to(ax3.c2p(0,0))
        cap3 = VGroup(Text("3D ball (sphere)").scale(0.5), MathTex(r"V_3(r)=\tfrac{4}{3}\pi r^3")).arrange(DOWN, buff=0.25)
        cap3.next_to(ax3, DOWN)
        g3 = VGroup(ax3, sphere_outline, cap3).to_edge(RIGHT, buff=0.6).shift(UP*0.5)
        self.play(Create(ax3), Create(sphere_outline), FadeIn(cap3))

        self.wait(0.8)

        # Big formula and intuition
        general = VGroup(
            MathTex(r"V_d(r)=\frac{\pi^{d/2}}{\Gamma(\frac d2+1)}\,r^d").scale(0.9),
            Text("For fixed r, the neighborhood volume scales ∝ r^d", slant=ITALIC).scale(0.5),
            Text("Higher d → you sweep a much larger region to gather 'neighbors'", slant=ITALIC).scale(0.5)
        ).arrange(DOWN, buff=0.25).to_edge(DOWN)
        self.play(Write(general))

        # Numeric ratios vs cube for intuition (r=1)
        # 1D: 2/2 = 1.00, 2D: π/4 ≈ 0.785, 3D: (4/3)π / 8 ≈ 0.524
        ratios = VGroup(
            Text("Ratio: inscribed ball / cube (r=1):").scale(0.5),
            MathTex(r"d=1:\; \frac{2}{2}=1.00,\quad d=2:\; \frac{\pi}{4}\approx0.785,\quad d=3:\; \frac{\tfrac{4}{3}\pi}{8}\approx0.524").scale(0.6)
        ).arrange(DOWN, buff=0.2).next_to(general, UP)
        self.play(FadeIn(ratios))
        self.wait(2)


# ---------- 5) OPTIONAL: MINKOWSKI BALLS IN 2D ----------
class MinkowskiBalls2D(Scene):
    def construct(self):
        title = Text("Neighborhood shape depends on the metric (p-norm)").to_edge(UP)
        self.play(FadeIn(title))

        ax = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=6, y_length=6,
            axis_config={"include_tip": True}
        ).to_edge(LEFT, buff=0.6)
        self.play(Create(ax))

        r = 1.5

        # L2: circle
        circle = Circle(radius=ax.x_axis.n2p(r)[0]-ax.x_axis.n2p(0)[0], color=BLUE).move_to(ax.c2p(0,0))
        l2_lbl = MathTex(r"p=2\;(\text{Euclidean})").scale(0.6).next_to(ax, DOWN)
        self.play(Create(circle), FadeIn(l2_lbl))
        self.wait(0.6)

        # L1: diamond |x|+|y|=r
        # Build polygon for |x|+|y|=r
        pts = [ax.c2p( r,  0),
               ax.c2p( 0,  r),
               ax.c2p(-r,  0),
               ax.c2p( 0, -r)]
        diamond = Polygon(*pts, color=YELLO*
