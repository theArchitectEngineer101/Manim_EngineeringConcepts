# 🌐 Laplace Transform Magnitude Surface (Manim Animation)

This Manim animation visualizes the magnitude of the Laplace Transform $F(s)$ as a 3D surface over the complex S-plane ($s = \sigma + j\omega$). It dynamically demonstrates how changes in the pole/zero location in the S-plane affect the shape of the surface, and how this relates to the corresponding time-domain signal $f(t)$.

## 🚀 Functionality

The `Laplace_Surface.py` script generates an animation that:

* **Displays $f(t)$ and the Complex S-Plane:** Shows the time-domain signal $f(t)$ on the left and the complex S-plane on the right.
* **Dynamic Pole Location:** A purple dot (`s = \sigma + j\omega`) moves on the S-plane, representing the real ($\sigma$) and imaginary ($\omega$) parts of a pole.
* **Synchronized Visuals:**
    * As the pole moves, the time-domain signal $f(t)$ (`e^{\sigma t} \cdot \sin(\omega t)`) dynamically updates to reflect the changing $\sigma$ (damping) and $\omega$ (frequency).
    * A 3D surface representing $|F(s)|$ (the magnitude of the Laplace Transform) is drawn over the S-plane, with its shape changing in real-time as the pole's location changes.
* **Exploration of Key Behaviors:** The animation includes sequences that demonstrate:
    * Changes in frequency ($\omega$).
    * Changes in damping ($\sigma$).
    * Special cases like purely oscillatory signals ($\sigma = 0$).
    * Different pole trajectories (e.g., elliptical, lemniscate) in the S-plane and their effects on the time-domain signal and Laplace surface.

## ▶️ How to Use

To render this animation, you need to have Manim installed.

1.  **Navigate to the project directory:**
    ```bash
    cd your_repo/Manim_EngineeringConcepts/LaplaceSurface/
    ```
2.  **Run Manim:**
    ```bash
    manim -pql Laplace_Surface.py LaplaceSurface
    ```
    * `-p`: Plays the animation after rendering.
    * `-q l`: Renders in "low quality" for faster preview. Use `-q h` for high quality, or `-q k` for 4K.
    * `LaplaceSurface`: The name of the class in the Python file.

## 📊 Visual Explanation

The animation effectively connects the visual representation of a pole/zero in the S-plane with the behavior of its corresponding time-domain signal and the magnitude of its Laplace Transform. It helps to intuitively grasp concepts like:

* Stability (related to the real part $\sigma$).
* Oscillation frequency (related to the imaginary part $\omega$).
* Resonance and poles.
