from styles.theme_manager import generate_stylesheet

# This file is kept for backward compatibility, but styles are now managed by ThemeManager
def get_stylesheet():
    # Default theme for fallback
    variables = {
        "--radius": "12px",
        "--background": "oklch(0.13 0.028 261.692)",
        "--foreground": "oklch(0.985 0.002 247.839)",
        "--card": "oklch(0.21 0.034 264.665)",
        "--card-foreground": "oklch(0.985 0.002 247.839)",
        "--primary": "#2dd4bf",
        "--primary-foreground": "oklch(0.21 0.034 264.665)",
        "--secondary": "#64748b",
        "--secondary-foreground": "oklch(0.985 0.002 247.839)",
        "--input": "oklch(1 0 0 / 15%)",
        "--border": "oklch(1 0 0 / 10%)",
        "--accent": "oklch(0.278 0.033 256.848)",
        "--accent-foreground": "oklch(0.985 0.002 247.839)"
    }
    return generate_stylesheet(variables)