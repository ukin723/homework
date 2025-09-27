import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle
from matplotlib.dates import DateFormatter, YearLocator
import matplotlib.font_manager as fm
from data_processing import fetch_sunspot_data, preprocess_data

# --------------------------
# 3. Artistic Visualization Design (Revised Version)
# --------------------------
def create_sunspot_animation(df, cycle_peaks):
    """Create an artistic sunspot activity animation (Revised Version)"""
    # Set the overall style
    plt.style.use('dark_background')
    
    # Use a more general font setting to avoid font warnings
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    if 'Arial' in available_fonts:
        plt.rcParams['font.family'] = 'Arial'
    elif 'DejaVu Sans' in available_fonts:
        plt.rcParams['font.family'] = 'DejaVu Sans'
    else:
        plt.rcParams['font.family'] = 'sans-serif'
    
    plt.rcParams['axes.facecolor'] = '#000011'
    plt.rcParams['figure.facecolor'] = '#000011'
    
    # Create the figure and main axes
    fig = plt.figure(figsize=(16, 12), dpi=100)
    ax = plt.subplot(111)
    
    # Create a custom colormap - from deep blue to gold
    colors = ['#000033', '#001144', '#003366', '#0066AA', '#00AAFF', '#33CCFF', '#FFCC00', '#FF9900', '#FF6600']
    cmap = LinearSegmentedColormap.from_list('sun_cmap', colors, N=256)
    
    # Add a starry background
    np.random.seed(42)  # Ensure reproducibility
    star_x = np.random.rand(300) * (df['date'].max() - df['date'].min()).days + df['date'].min().toordinal()
    star_y = np.random.rand(300) * df['sunspot_area'].max() * 1.2
    star_sizes = np.random.rand(300) * 20 + 5
    star_alphas = np.random.rand(300) * 0.7 + 0.3
    
    for i in range(len(star_x)):
        ax.plot(star_x[i], star_y[i], 'o', markersize=star_sizes[i] * 0.1, 
                alpha=star_alphas[i], color='white', markeredgewidth=0)
    
    # Create the solar disk background
    sun_disk = Circle((df['date'].mean().toordinal(), df['sunspot_area'].max()/2), 
                     radius=(df['date'].max() - df['date'].min()).days/3, 
                     color='#331100', alpha=0.2, zorder=0)
    ax.add_patch(sun_disk)
    
    # Initialize chart elements
    line, = ax.plot([], [], color=cmap(0.8), linewidth=3.5, alpha=0.9, 
                    label='Sunspot Activity', zorder=5, solid_capstyle='round')
    
    # Initialize the filled area
    fill = ax.fill_between([], [], [], color=cmap(0.5), alpha=0.3, zorder=4)
    
    # Add cycle text
    cycle_text = ax.text(0.02, 0.96, '', transform=ax.transAxes, 
                         fontsize=16, color='#FFCC00', fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.5', facecolor=(0.1, 0.1, 0.3, 0.7), edgecolor='#FFCC00', linewidth=1))
    
    # Add date text
    date_text = ax.text(0.02, 0.88, '', transform=ax.transAxes, 
                        fontsize=14, color='#33CCFF', fontweight='normal')
    
    # Set axis labels
    ax.set_xlabel('Time (Year)', fontsize=14, color='#CCCCFF', labelpad=15)
    ax.set_ylabel('Sunspot Area (Millionths of a Solar Hemisphere)', fontsize=14, color='#CCCCFF', labelpad=15)
    ax.set_title('Solar Dance: 274 Years of Sunspot Activity\nSolar Cycles and Cosmic Rhythm', 
                 fontsize=20, color='#FFCC00', pad=30, fontweight='bold')
    
    # Beautify the axes
    ax.spines['bottom'].set_color('#4444AA')
    ax.spines['left'].set_color('#4444AA')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.tick_params(axis='both', colors='#8888FF', labelsize=12)
    ax.grid(True, color='#222266', linestyle='--', linewidth=0.5, alpha=0.5)
    
    ax.xaxis.set_major_locator(YearLocator(25))
    ax.xaxis.set_major_formatter(DateFormatter('%Y'))
    y_max = df['sunspot_area'].max() * 1.15
    ax.set_ylim(0, y_max)
    ax.set_xlim(df['date'].min(), df['date'].max())
    
    # Add legend
    legend = ax.legend(loc='upper right', fontsize=12, framealpha=0.8, 
                      facecolor=(0.05, 0.05, 0.2), edgecolor='#FFCC00', 
                      labelcolor='#CCCCFF')
    
    # Add attribution
    fig.text(0.99, 0.01, 'Data Source: SILSO | Visualization: Solar Art Project', 
             ha='right', va='bottom', color='#6666AA', fontsize=10)
    
    # Animation update function
    def update(frame):
        current_idx = min(frame * 3, len(df)-1)  # Advance 3 months per frame
        current_data = df.iloc[:current_idx+1]
        x_data = current_data['date']
        y_data = current_data['sunspot_area']
        
        # Update the main curve
        line.set_data(x_data, y_data)
        
        # Update the filled area - using a simple method
        # Clear old fills
        for collection in ax.collections:
            if collection != fill:  # Keep other collections (if any)
                collection.remove()
        
        # Create new fills
        ax.fill_between(x_data, 0, y_data, color=cmap(0.5), alpha=0.3, zorder=4)
        
        # Update text
        current_cycle = current_data['cycle'].iloc[-1] if not pd.isna(current_data['cycle'].iloc[-1]) else 'Unknown'
        cycle_text.set_text(f'Current Solar Cycle: {int(current_cycle) if current_cycle != "Unknown" else current_cycle}')
        
        current_date = current_data['date'].iloc[-1]
        date_text.set_text(f'{current_date.strftime("%Y %B")}\nActivity Level: {y_data.iloc[-1]:.1f}')
        
        # Dynamically change line color based on the current value
        norm_value = y_data.iloc[-1] / y_max
        line.set_color(cmap(norm_value))
        
        return line, cycle_text, date_text
    
    # Create animation - disable blit to avoid compatibility issues
    frames = len(df) // 3
    anim = animation.FuncAnimation(
        fig, update, frames=frames, interval=100,
        blit=False, repeat=True  # Disable blit
    )
    
    plt.tight_layout()
    
    # Save the animation
    try:
        anim.save('solar_art.gif', writer='pillow', dpi=100, fps=10, 
                  savefig_kwargs={'facecolor': '#000011'})
        print("Artistic visualization saved as: solar_art.gif")
    except Exception as e:
        print(f"Failed to save animation: {e}")
    
    plt.show()

# --------------------------
# Main Execution Logic
# --------------------------
if __name__ == "__main__":
    sunspot_df = fetch_sunspot_data()
    processed_df, cycle_peaks = preprocess_data(sunspot_df)
    create_sunspot_animation(processed_df, cycle_peaks)