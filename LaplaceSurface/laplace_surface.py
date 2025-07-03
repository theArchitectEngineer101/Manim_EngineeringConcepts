from manim import *
from manim.utils.color import color_gradient
import numpy as np

config.frame_rate = 30
config.pixel_height = 720
config.pixel_width = 1280

class LaplaceSurface(ThreeDScene):
    def construct(self):
        # rainbow_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

        # def rainbow_color(u, v):
        #     # Normaliza u e v para [0,1] baseado nos ranges
        #     u_norm = (u + magic_x*dinamic_scale_x.get_value()) / (2*magic_x*dinamic_scale_x.get_value())
        #     v_norm = (v + magic_y*dinamic_scale_y.get_value()) / (2*magic_y*dinamic_scale_y.get_value())
            
        #     # Combina u e v para criar um padrão interessante
        #     color_progress = (u_norm + v_norm) % 1.0
        #     return color_gradient(rainbow_colors, color_progress)
        
        # def rainbow_z_based(u, v):
        #     z_value = F_mod(u, v)
        #     z_normalized = (z_value + z_max.get_value()) / (2*z_max.get_value())
        #     return color_gradient(rainbow_colors, z_normalized)

        # --- ValueTrackers para alpha, omega e escala ---
        alpha = ValueTracker(0.3) # Controle da escala exponencial
        omega = ValueTracker(0.5) # Controle da escala de frequencia
        dinamic_scale_x = ValueTracker(1.0) # Controle de escala dinamica em x
        dinamic_scale_y = ValueTracker(1.0) # Controle de escala dinamica em y
        surface_scale = ValueTracker(0.5)

        magic_x = 5 # x_lim do plano e surf.
        magic_y = 5 # y_lim do plano e surf.
        z_max = ValueTracker(3) # z_max da superficie

        # Parâmetros de controle da trajetória
        self.m = 2.0
        self.n = 2.0
        
        #===========================================================================================================================================
        #                                                    Conj. de Definições 2D
        #===========================================================================================================================================

        # --- Configuracao dos eixos do grafico f(t) (ESQUERDA) ---
        axes = Axes(
            x_range=[0, magic_x],
            y_range=[-magic_y, magic_y],
            x_length=5,
            y_length=5,
            axis_config={"color": BLUE},
            tips=False
        ).shift(LEFT * 3.5)
        labels = axes.get_axis_labels(x_label="t", y_label="f(t)")


        # Funcao principal que sera analisada
        def func(t):
            raw_value = np.exp(alpha.get_value() * t) * np.sin(omega.get_value() * t)

            # Limitação suave com sinal preservado
            threshold = 4.9  # Um pouco menor que 5 para margem visual
            if raw_value > threshold:
                return threshold
            elif raw_value < -threshold:
                return -threshold
            return raw_value

        # Criação do gráfico com limitação garantida
        graph = always_redraw(lambda: 
            axes.plot(
                func,
                x_range=[0, magic_x],
                use_vectorized=False  # Importante para a limitação personalizada
            )
            .set_stroke(width=3, color=PINK)
            .set_stroke(opacity=0.8)
        )

        #===========================================================================================================================================
        #                                                       Plano Complexo
        #===========================================================================================================================================
        # --- Plano Complexo com escala dinamica (DIREITA) ---
        # Construção de plano updater para aplicação de escala dinamica
        def update_plane(mob):
            new_plane = ComplexPlane(
                x_range=[-magic_x*dinamic_scale_x.get_value(), magic_x*dinamic_scale_x.get_value()],
                y_range=[-magic_y*dinamic_scale_y.get_value(), magic_y*dinamic_scale_y.get_value()],
                x_length=5,
                y_length=5,
                background_line_style={"stroke_opacity": 0.3}
            ).shift(RIGHT * 3.5)
            mob.become(new_plane)
        # Plano complexo atualizado através de .add_updater()
        complex_plane = ComplexPlane(
            x_range=[-magic_x, magic_x],
            y_range=[-magic_y, magic_y],
            x_length=5,
            y_length=5,
            background_line_style={"stroke_opacity": 0.3}
        ).shift(RIGHT * 3.5)
        complex_plane.add_updater(update_plane)

        #===========================================================================================================================================
        #                                                      Conj. de Definicoes 3D
        #===========================================================================================================================================

        # Função |F(s)|: módulo da transformada de Laplace
        def F_mod(x, y):
            s = complex(x, y)
            a = alpha.get_value()
            w = omega.get_value()
            denom = (s - a)**2 + w**2
            threshold = 1e-7
            safe_denom = denom if abs(denom) > threshold else threshold * (1 + 1j)
            return min(abs(w / safe_denom), z_max.get_value())
        
                # Função |F(s)|: módulo da transformada de Laplace
        def F_mod2(x, y):
            s = complex(x, y)
            a = alpha.get_value() / 2
            w = omega.get_value() / 2
            denom = (s - a)**2 + w**2
            threshold = 1e-7
            safe_denom = denom if abs(denom) > threshold else threshold * (1 + 1j)
            return min(abs(w / safe_denom), z_max.get_value())

        # Centro do plano calculado uma única vez fora do always_redraw
        plane_center = complex_plane.get_center()

        # # Objeto que aplica o gradiente
        # class RainbowSurface(Surface):
        #     def __init__(self, *args, **kwargs):
        #         super().__init__(*args, **kwargs)
        #         self.rainbow_colors = rainbow_colors
                
        #     def point_to_color(self, point):
        #         # Converte coordenadas 3D para progressão no gradiente
        #         x, y, z = point
        #         progress = (x + y) % 1.0  # Padrão diagonal
        #         return color_gradient(self.rainbow_colors, progress)
            
        # class RainbowSurface(Surface):
        #     def __init__(self, func, u_range, v_range, resolution, **kwargs):
        #         super().__init__(func, u_range=u_range, v_range=v_range, resolution=resolution, **kwargs)
                
        #         # Define as cores do arco-íris
        #         self.rainbow_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        #         # self.rainbow_colors = [
        #         #     "#FF0000", "#FF7F00", "#FFFF00", 
        #         #     "#00FF00", "#0000FF", "#4B0082", "#9400D3"
        #         # ]
                
        #         # Aplica o gradiente diagonal
        #         self.set_color_by_xyz_func(
        #             lambda point: color_gradient(
        #                 self.rainbow_colors,
        #                 (point[0] + point[1]) % 1.0  # Padrão diagonal simples
        #             )
        #         )

        # Superficie 3D com always_redraw
        surface = always_redraw(lambda:
            Surface(
                lambda u, v: np.array([
                    (u * surface_scale.get_value()) + plane_center[0],  # Scale e shift incorporados
                    (v * surface_scale.get_value()) + plane_center[1],  # diretamente nas coordenadas
                    F_mod(u, v)
                ]),
                u_range=[
                    -magic_x*dinamic_scale_x.get_value(),
                     magic_x*dinamic_scale_x.get_value()
                ],
                v_range=[
                    -magic_y*dinamic_scale_y.get_value(),
                     magic_y*dinamic_scale_y.get_value()
                ],
                resolution=(45, 45),
                fill_opacity=0.9,
                stroke_color=BLACK,
                stroke_width=0.0,
                checkerboard_colors=["#00CCFF", "#8400FF"],
                # fill_color=lambda u, v: color_gradient(
                #     rainbow_colors,
                #     (np.sin(np.sqrt(u**2 + v**2)) + 1) / 2  # valor ∈ [0, 1]
                # ),
                # fill_color=lambda u, v: rainbow_color(u, v),  # Aplicação direta do gradiente
                # fill_color=lambda u, v: rainbow_z_based(u, v)
                # color_pattern="height_based"
            )
        )

        # Superficie 3D com always_redraw
        surface2 = always_redraw(lambda:
            Surface(
                lambda u, v: np.array([
                    u * surface_scale.get_value(),
                    v * surface_scale.get_value(),
                    F_mod2(u, v)
                ]),
                u_range=[
                    -magic_x*dinamic_scale_x.get_value(),
                     magic_x*dinamic_scale_x.get_value()
                ],
                v_range=[
                    -magic_y*dinamic_scale_y.get_value(),
                     magic_y*dinamic_scale_y.get_value()
                ],
                resolution=(60, 60),
                fill_opacity=0.9,
                stroke_color=BLACK,
                stroke_width=0.0,
                checkerboard_colors=["#00CCFF", "#8400FF"],
                # fill_color=lambda u, v: color_gradient(
                #     rainbow_colors,
                #     (np.sin(np.sqrt(u**2 + v**2)) + 1) / 2  # valor ∈ [0, 1]
                # ),
                # fill_color=lambda u, v: rainbow_color(u, v),  # Aplicação direta do gradiente
                # fill_color=lambda u, v: rainbow_z_based(u, v)
                # color_pattern="height_based"
            )
        )



        #===========================================================================================================================================
        #                                                        dot e dot_updaters
        #===========================================================================================================================================

        # Ponto com limites dinamicos baseados na escala
        dot = always_redraw(lambda:
            Dot(
                complex_plane.n2p(
                    complex(
                        alpha.get_value()/dinamic_scale_x.get_value(),
                        omega.get_value()/dinamic_scale_y.get_value(),
                    )),
                color=PURPLE,
                radius=0.1
            )
        )

        # Define uma trajetória parametrizada eliptica
        def dot_elipse_update(mob, t):
            # Define valores de alpha e omega ao longo da trajetória
            a = self.m * np.cos(t)  # Parte real
            w = self.n * np.sin(t)  # Parte imaginária
            # Atualiza os ValueTrackers (para sincronizar a superfície 3D)
            alpha.set_value(a)
            omega.set_value(w)
            # Posiciona o ponto no grid (complex_plane)
            mob.move_to(complex_plane.n2p(complex(a, w)))

        # Define uma trajetória parametrizada lemniscata
        def dot_lemniscate_update(mob, t):
            # Parâmetros da lemniscata (ajuste conforme necessário)
            a = 9.0  # Tamanho da lemniscata
            scale_factor = 1.0  # Escala geral
            
            # Equações paramétricas da lemniscata
            y = (a * np.cos(t)) / (1 + np.sin(t)**2)
            x = (a * np.sin(t) * np.cos(t)) / (1 + np.sin(t)**2)
            
            # Aplica escala e atualiza ValueTrackers
            alpha.set_value(x * scale_factor)
            omega.set_value(y * scale_factor)
            
            # Move o ponto
            mob.move_to(complex_plane.n2p(complex(x * scale_factor, y * scale_factor)))

        #===========================================================================================================================================
        #                                                     Rótulos e Eqs.
        #===========================================================================================================================================

        # Equacao dinamica f(t) (centralizada no topo)
        equation = always_redraw(lambda:
            MathTex(
                r"f(t) = e^{", 
                f"{alpha.get_value():.2f}", # utilizacao de f string
                r"t} \cdot \sin(",
                f"{omega.get_value():.2f}",
                r"t)"
            ).to_edge(UP)
        )

        # # Equação dinâmica da Transformada de Laplace F(s)
        # laplace_transform = always_redraw(lambda:
        #     MathTex(
        #         rf"F(s) = \frac{{{omega.get_value():.2f}}}{{(s - {alpha.get_value():.2f})^2 + {omega.get_value():.2f}^2}}"
        #     ).scale(0.7).set_color(BLUE).to_edge(DOWN)
        # )

        # Rotulo compacto para o ponto
        dot_label = always_redraw(lambda:
            MathTex(
                r"s = ",
                f"{alpha.get_value():.2f}", # f string
                r" + ", # r string
                f"{omega.get_value():.2f}",
                r"i"
            ).next_to(dot, UP, buff=0.1).scale(0.5)
        )

        # Linhas auxiliares definidas a partir de eixo e ponto
        h_line = always_redraw(lambda:
            Line(
                start=complex_plane.n2p(complex(0, omega.get_value()/dinamic_scale_y.get_value())),  # Comeca no eixo y (omega)
                end=complex_plane.n2p(complex(alpha.get_value()/dinamic_scale_x.get_value(), omega.get_value()/dinamic_scale_y.get_value())),  # Termina no ponto
                color=YELLOW,
                stroke_width=1.5
            )
        )
        v_line = always_redraw(lambda:
            Line(
                start=complex_plane.n2p(complex(alpha.get_value()/dinamic_scale_x.get_value(), 0)),
                end=complex_plane.n2p(complex(alpha.get_value()/dinamic_scale_x.get_value(), omega.get_value()/dinamic_scale_y.get_value())),
                color=YELLOW,
                stroke_width=1.5
            )
        )

        #===========================================================================================================================================
        #                                                         Seq. de Animacoes 2D
        #===========================================================================================================================================
        
        # Introduz eixos e plano complexo
        self.play(
            Create(axes),
            Write(labels),
            Create(complex_plane),
            run_time=1.5
        )
        self.wait(1.5)

        # Desenha o gráfico inicial e pólo
        self.play(
            Write(equation),
            Create(graph),
            FadeIn(dot),
            Write(dot_label),
            Create(h_line),
            Create(v_line),
            run_time=2
        )
        self.wait(1.5)

        # Aumento e reducao da frequencia
        self.play(
            omega.animate.set_value(10.0),
            dinamic_scale_y.animate.set_value(3.0),  # Ajuste de escala y
            run_time=6,
            rate_func=linear
        )
        self.play(
            omega.animate.set_value(-4),
            dinamic_scale_y.animate.set_value(1.0),  # Ajuste de escala y
            run_time=7,
            rate_func=linear
        )
        self.wait(1.5)

        # Reducao e aumento da exponencial
        self.play(
            alpha.animate.set_value(-2.0),
            run_time=4,
            rate_func=linear
        )
        self.play(
            alpha.animate.set_value(0.3),
            run_time=3,
            rate_func=linear
        )
        self.wait(3)

        # Aumento exagerado da exponencial
        self.play(
            alpha.animate.set_value(2.0),
            run_time=3,
            rate_func=linear
        )
        self.wait(1)

        # Reducao exagerada da exponencial
        self.play(
            alpha.animate.set_value(-5.0),
            dinamic_scale_x.animate.set_value(1.5),
            run_time=6,
            rate_func=linear
        )
        self.wait(1.5)
        # Reducao mais exagerada da exponencial
        self.play(
            alpha.animate.set_value(-10.0),
            dinamic_scale_x.animate.set_value(3.0),
            run_time=4,
            rate_func=rush_into
        )
        self.wait(1.5)        

        # Caso especial de exponencial nula
        self.play(
            alpha.animate.set_value(0.0),
            dinamic_scale_x.animate.set_value(1.0),
            run_time=7,
            rate_func=linear
        )
        self.wait(2)
        # Controle de frequencia com alpha nulo
        self.play(
            omega.animate.set_value(0),
            run_time=6,
            rate_func=linear
        )
        self.wait(2)
        self.play(
            omega.animate.set_value(2.5),
            run_time=3,
            rate_func=linear
        )
        self.wait(1.5)

        # Demonstração de controle da escala
        self.play(
            dinamic_scale_x.animate.set_value(0.5),  # Ajuste de escala x
            dinamic_scale_y.animate.set_value(0.5),  # Ajuste de escala y
            run_time=1.5,
            rate_func=linear
        )
        self.wait(0.5)
        self.play(
            dinamic_scale_x.animate.set_value(1.0),  # Ajuste de escala x
            dinamic_scale_y.animate.set_value(1.0),  # Ajuste de escala y
            run_time=1.5,
            rate_func=linear
        )
        self.wait(10)

        #===========================================================================================================================================
        #                                                    TRANSIÇÃO PARA AMBIENTE 3D
        #===========================================================================================================================================

        self.add_fixed_in_frame_mobjects(axes, graph, equation, labels)

        # Plano 3D e F(s) são colocados na tela
        self.play(
            #Write(laplace_transform),
            FadeOut(dot_label),
            run_time=3.0
        )

        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=3)
        self.wait(1.5)

        #=======================================
        # [BLOCO 1] ANIMAÇÃO DO PONTO CAMINHANDO NO PLANO
        #=======================================

        self.play(
            UpdateFromAlphaFunc(
                dot,
                lambda mob, alpha: dot_elipse_update(mob, alpha * 2 * PI),
                run_time=16,
                rate_func=linear
            ),
        )
        self.wait(3)

        #=======================================
        # [BLOCO 2] CRIAÇÃO DA SUPERFÍCIE F(s)
        #=======================================

        self.play(FadeIn(surface), run_time=5)

        self.play(
            UpdateFromAlphaFunc(
                dot,
                lambda mob, alpha: dot_elipse_update(mob, alpha * 2 * PI),
                run_time=16,
                rate_func=linear
            ),
        )
        self.wait(3)

        # Demonstração de controle da escala
        z_max.set_value(2*z_max.get_value())
        self.play(
            surface_scale.animate.set_value(0.25), # Ajuste de escala surf
            dinamic_scale_x.animate.set_value(2.0),  # Ajuste de escala x
            dinamic_scale_y.animate.set_value(2.0),  # Ajuste de escala y
            run_time=4.0,
            rate_func=linear
        )
        self.wait(1)


        self.m = 5.8  # Novo valor para m
        self.n = 6.2  # Novo valor para n
        self.play(
            UpdateFromAlphaFunc(
                dot,
                lambda mob, alpha: dot_elipse_update(mob, alpha * 4 * PI),
                run_time=48,
                rate_func=linear
            ),
        )

        self.play(
            FadeOut(axes, graph, equation, labels, surface, complex_plane, h_line, v_line, dot),
            run_time=2,
            rate_func=linear
        )

        complex_plane.shift(LEFT * 3.5)
        surface_scale.set_value(0.5)
        self.wait(1)

        self.play(
            FadeIn(surface2),
            run_time=1,
            rate_func=linear
        )

        self.play(
            UpdateFromAlphaFunc(
                dot,
                lambda mob, alpha: dot_lemniscate_update(mob, alpha * 6 * PI),  # 1 volta completa
                run_time=128,
                rate_func=linear
            ),
        )      

        self.wait(10)