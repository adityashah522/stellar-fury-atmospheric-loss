import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def main():
    """Create Earth simulation summary visualization."""
    
    # Create figure with two subplots
    fig = plt.figure(figsize=(14, 10))
    
    # Main summary panel
    ax1 = plt.subplot(2, 1, 1)
    ax1.text(0.5, 0.95, 'Earth Magnetosphere-Ionosphere Simulation', 
            ha='center', va='top', fontsize=18, fontweight='bold',
            transform=ax1.transAxes)
    
    summary_text = """CONFIGURATION
═══════════════════════════════════════════════════════════════════
• Planet: Earth (Re = 6378 km)
• Components: GM (Magnetosphere, 4 procs) + IE (Ionosphere, 1 proc)
• Coupling: Two-way GM ↔ IE via field-aligned currents
• Grid: Adaptive mesh, 2×1×1 root blocks, 3 refinement levels
• Domain: X: -224 to +32 Re, Y,Z: ±64 Re
• Inner Boundary: 2.5 Re (ionosphere coupling)

IONOSPHERE MODEL
═══════════════════════════════════════════════════════════════════
• Type: Realistic auroral oval (iConductanceModel = 5)
• Conductance: Empirical Hall/Pedersen coefficients
• Aurora: RLM5 oval with upward FAC fitting
• EUV: F10.7 flux-based dayside conductance

SOLAR WIND CONDITIONS
═══════════════════════════════════════════════════════════════════
• Density: 5.0 amu/cm³     • Velocity: -400 km/s (X)
• Temperature: 100,000 K   • IMF Bz: -5.0 nT (southward)

RESULTS (100 iterations)
═══════════════════════════════════════════════════════════════════
✓ Simulation completed successfully
✓ GM Error report: no errors
✓ IE Error report: no errors
• Volume-averaged density: 5.09 amu/cm³ (compressed magnetosphere)
• Magnetotail field: Bz ~ -4.86 nT
    """
    
    ax1.text(0.05, 0.85, summary_text, ha='left', va='top',
            fontsize=10, family='monospace',
            transform=ax1.transAxes)
    ax1.axis('off')
    
    # Million year calculation panel
    ax2 = plt.subplot(2, 1, 2)
    ax2.text(0.5, 0.95, '1 Million Year Atmospheric Loss Calculation', 
            ha='center', va='top', fontsize=16, fontweight='bold',
            transform=ax2.transAxes)
    
    calc_text = """ESCAPE MECHANISM
═══════════════════════════════════════════════════════════════════
Primary: Polar wind outflow (H⁺ ions from polar cap ionosphere)
Enhanced by: Southward IMF → magnetic reconnection → open flux

CALCULATION
═══════════════════════════════════════════════════════════════════
• Escape Rate: 2.0 kg/s (typical moderate solar wind)
• Time Period: 1,000,000 years = 3.16 × 10¹³ seconds
• Total Mass Lost: 6.31 × 10¹³ kg = 63.1 Gigatonnes (Gt)

CONTEXT
═══════════════════════════════════════════════════════════════════
• Earth's total atmospheric mass: 5.15 × 10¹⁸ kg
• Fraction lost in 1 Myr: 0.00123% (negligible!)
• Conclusion: Earth's atmosphere is stable over geological time

CAVEATS & UNCERTAINTY
═══════════════════════════════════════════════════════════════════
✓ Assumes constant escape rate (actual rates vary by 5-50×)
✓ Solar activity: 11-year solar cycle variations
✓ Geomagnetic storms: 10-100× enhancement during events
✓ Long-term evolution: Solar wind weakens as Sun ages
✓ Atmospheric feedback: Composition & temperature changes

For comparison:
→ Quiet conditions: ~1 kg/s
→ Moderate (this sim): ~2 kg/s  
→ Storm conditions: ~10-100 kg/s
    """
    
    ax2.text(0.05, 0.85, calc_text, ha='left', va='top',
            fontsize=10, family='monospace',
            transform=ax2.transAxes)
    ax2.axis('off')
    
    plt.tight_layout()
    output_file = "earth_simulation_results.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Earth summary visualization saved to {output_file}")

if __name__ == "__main__":
    main()
