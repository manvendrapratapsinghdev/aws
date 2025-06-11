import streamlit as st
import subprocess
import json
import pandas as pd
import time
from datetime import datetime
import altair as alt
import platform

# Set page config
st.set_page_config(
    page_title="Wi-Fi Scanner",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
        background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .wifi-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .wifi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.12);
    }
    .signal-strength {
        font-size: 24px;
        font-weight: bold;
    }
    .metrics-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin: 20px 0;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        flex: 1;
        min-width: 150px;
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    .header {
        margin-bottom: 30px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def get_signal_icon(signal_strength):
    """Return appropriate Wi-Fi signal icon based on signal strength."""
    if signal_strength >= -50:
        return "📶"  # Excellent
    elif signal_strength >= -60:
        return "📶"  # Good
    elif signal_strength >= -70:
        return "📶"  # Fair
    else:
        return "📶"  # Poor

def get_signal_quality(signal_strength):
    """Convert signal strength to quality category."""
    if signal_strength >= -50:
        return "Excellent"
    elif signal_strength >= -60:
        return "Good"
    elif signal_strength >= -70:
        return "Fair"
    else:
        return "Poor"

def get_security_info(network):
    """Extract security information."""
    security = []
    
    if "WPA2" in network.get("security", ""):
        security.append("WPA2")
    if "WPA3" in network.get("security", ""):
        security.append("WPA3")
    if "WPA" in network.get("security", "") and "WPA2" not in network.get("security", "") and "WPA3" not in network.get("security", ""):
        security.append("WPA")
    if "WEP" in network.get("security", ""):
        security.append("WEP")
    
    if not security and network.get("security", "") != "":
        security = [network.get("security", "")]
    
    return ", ".join(security) if security else "Open"

def scan_wifi_networks():
    """Scan for Wi-Fi networks using appropriate command based on OS."""
    try:
        os_name = platform.system()
        
        if os_name == "Darwin":  # macOS
            cmd = ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            lines = result.stdout.strip().split('\n')
            headers = lines[0].split()
            
            networks = []
            for line in lines[1:]:
                fields = line.split()
                if len(fields) >= 5:
                    ssid = ' '.join(fields[0:-4])
                    bssid = fields[-4]
                    rssi = int(fields[-3])
                    channel = fields[-2]
                    security = fields[-1]
                    
                    networks.append({
                        "ssid": ssid,
                        "bssid": bssid,
                        "signal_strength": rssi,
                        "channel": channel,
                        "security": security,
                        "frequency_band": "2.4 GHz" if int(channel) <= 14 else "5 GHz"
                    })
            
            return networks
            
        elif os_name == "Linux":
            cmd = ["sudo", "iwlist", "wlan0", "scan"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Parsing logic for Linux
            networks = []
            current_network = {}
            
            for line in result.stdout.strip().split('\n'):
                line = line.strip()
                
                if "Cell" in line and "Address" in line:
                    if current_network and "ssid" in current_network:
                        networks.append(current_network)
                    current_network = {"bssid": line.split("Address: ")[1].strip()}
                
                elif "ESSID:" in line:
                    current_network["ssid"] = line.split('ESSID:"')[1].split('"')[0]
                
                elif "Signal level=" in line:
                    level_part = line.split("Signal level=")[1].split()[0]
                    if "dBm" in level_part:
                        current_network["signal_strength"] = int(level_part.replace("dBm", ""))
                    else:
                        # Convert to dBm if needed
                        value = int(level_part.split("/")[0])
                        current_network["signal_strength"] = -100 + value * 2  # Approximate conversion
                
                elif "Channel:" in line:
                    current_network["channel"] = line.split("Channel:")[1].strip()
                    channel = int(current_network["channel"])
                    current_network["frequency_band"] = "2.4 GHz" if channel <= 14 else "5 GHz"
                
                elif "IE: " in line and ("WPA" in line or "IEEE 802.11i/WPA2" in line or "WEP" in line):
                    if "security" not in current_network:
                        current_network["security"] = line.split("IE: ")[1].strip()
                    else:
                        current_network["security"] += ", " + line.split("IE: ")[1].strip()
            
            if current_network and "ssid" in current_network:
                networks.append(current_network)
            
            return networks
            
        elif os_name == "Windows":
            # Use netsh for Windows
            cmd = ["netsh", "wlan", "show", "networks", "mode=Bssid"]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True)
            
            # Parsing logic for Windows
            networks = []
            current_network = {}
            
            for line in result.stdout.strip().split('\n'):
                line = line.strip()
                
                if "SSID" in line and ":" in line and "BSSID" not in line:
                    if current_network and "ssid" in current_network:
                        networks.append(current_network)
                    current_network = {"ssid": line.split(":", 1)[1].strip()}
                
                elif "BSSID" in line and ":" in line:
                    current_network["bssid"] = line.split(":", 1)[1].strip()
                
                elif "Signal" in line and ":" in line:
                    signal_percent = int(line.split(":", 1)[1].strip().replace("%", ""))
                    # Convert percentage to dBm (approximation)
                    current_network["signal_strength"] = -100 + signal_percent / 2
                
                elif "Channel" in line and ":" in line:
                    current_network["channel"] = line.split(":", 1)[1].strip()
                    channel = int(current_network["channel"])
                    current_network["frequency_band"] = "2.4 GHz" if channel <= 14 else "5 GHz"
                
                elif "Authentication" in line and ":" in line:
                    current_network["security"] = line.split(":", 1)[1].strip()
            
            if current_network and "ssid" in current_network:
                networks.append(current_network)
            
            return networks
        
        else:
            st.error(f"Unsupported operating system: {os_name}")
            return []
            
    except subprocess.CalledProcessError as e:
        st.error(f"Error running Wi-Fi scan command: {e}")
        if "permission denied" in str(e).lower() or "not permitted" in str(e).lower():
            st.error("This app requires sudo/admin privileges to scan Wi-Fi networks.")
        return []
    except Exception as e:
        st.error(f"Error scanning Wi-Fi networks: {e}")
        return []

def display_network_list(networks):
    """Display all networks in a table."""
    if not networks:
        st.warning("No Wi-Fi networks found.")
        return
    
    # Prepare data for the table
    data = []
    for network in networks:
        data.append({
            "SSID": network.get("ssid", "Unknown"),
            "Signal": f"{network.get('signal_strength', 0)} dBm",
            "Quality": get_signal_quality(network.get("signal_strength", -100)),
            "Channel": network.get("channel", "Unknown"),
            "Band": network.get("frequency_band", "Unknown"),
            "Security": get_security_info(network),
            "BSSID": network.get("bssid", "Unknown")
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Display table
    st.markdown("### All Wi-Fi Networks")
    st.dataframe(df, use_container_width=True)

def display_network_cards(networks):
    """Display networks as cards."""
    if not networks:
        st.warning("No Wi-Fi networks found.")
        return
    
    # Sort networks by signal strength (strongest first)
    sorted_networks = sorted(networks, key=lambda x: x.get('signal_strength', -100), reverse=True)
    
    # Display top networks as cards
    st.markdown("### Strongest Networks")
    
    # Use columns for responsive layout
    cols = st.columns(3)
    
    for idx, network in enumerate(sorted_networks[:6]):  # Show top 6 networks
        with cols[idx % 3]:
            signal_strength = network.get('signal_strength', -100)
            quality = get_signal_quality(signal_strength)
            icon = get_signal_icon(signal_strength)
            
            st.markdown(f"""
            <div class="wifi-card">
                <h3>{network.get('ssid', 'Unknown')}</h3>
                <div class="signal-strength">{icon} {signal_strength} dBm ({quality})</div>
                <p>Channel: {network.get('channel', 'Unknown')} ({network.get('frequency_band', 'Unknown')})</p>
                <p>Security: {get_security_info(network)}</p>
                <p>BSSID: {network.get('bssid', 'Unknown')}</p>
            </div>
            """, unsafe_allow_html=True)

def create_metrics(networks):
    """Create metrics display."""
    if not networks:
        return
    
    total_networks = len(networks)
    networks_2ghz = len([n for n in networks if n.get('frequency_band') == '2.4 GHz'])
    networks_5ghz = len([n for n in networks if n.get('frequency_band') == '5 GHz'])
    
    # Calculate channel distribution
    channel_distribution = {}
    for network in networks:
        channel = network.get('channel', 'Unknown')
        if channel != 'Unknown':
            if channel in channel_distribution:
                channel_distribution[channel] += 1
            else:
                channel_distribution[channel] = 1
    
    most_used_channel = max(channel_distribution.items(), key=lambda x: x[1])[0] if channel_distribution else 'None'
    
    # Security metrics
    open_networks = len([n for n in networks if get_security_info(n) == 'Open'])
    secure_networks = total_networks - open_networks
    
    # Display metrics
    st.markdown("### Network Statistics")
    
    st.markdown("""
    <div class="metrics-container">
        <div class="metric-card">
            <div class="metric-label">Total Networks</div>
            <div class="metric-value">{}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">2.4 GHz Networks</div>
            <div class="metric-value">{}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">5 GHz Networks</div>
            <div class="metric-value">{}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Most Used Channel</div>
            <div class="metric-value">{}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Secure Networks</div>
            <div class="metric-value">{} <small>({}%)</small></div>
        </div>
    </div>
    """.format(
        total_networks,
        networks_2ghz,
        networks_5ghz,
        most_used_channel,
        secure_networks,
        int(secure_networks / total_networks * 100) if total_networks > 0 else 0
    ), unsafe_allow_html=True)

def create_charts(networks):
    """Create data visualizations."""
    if not networks:
        return
        
    # Channel distribution chart
    st.markdown("### Channel Distribution")
    
    channel_data = {}
    for network in networks:
        channel = network.get('channel', 'Unknown')
        band = network.get('frequency_band', 'Unknown')
        
        if channel != 'Unknown':
            key = f"Channel {channel} ({band})"
            if key in channel_data:
                channel_data[key] += 1
            else:
                channel_data[key] = 1
    
    if channel_data:
        chart_data = pd.DataFrame({
            'Channel': list(channel_data.keys()),
            'Count': list(channel_data.values())
        })
        
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Channel:N', sort='-y'),
            y='Count:Q',
            color=alt.Color('Channel:N', legend=None),
            tooltip=['Channel', 'Count']
        ).properties(
            height=300
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
    
    # Signal strength distribution
    st.markdown("### Signal Strength Distribution")
    
    signal_categories = {
        'Excellent (-50 dBm or higher)': 0,
        'Good (-60 to -51 dBm)': 0,
        'Fair (-70 to -61 dBm)': 0,
        'Poor (below -70 dBm)': 0
    }
    
    for network in networks:
        signal = network.get('signal_strength', -100)
        
        if signal >= -50:
            signal_categories['Excellent (-50 dBm or higher)'] += 1
        elif signal >= -60:
            signal_categories['Good (-60 to -51 dBm)'] += 1
        elif signal >= -70:
            signal_categories['Fair (-70 to -61 dBm)'] += 1
        else:
            signal_categories['Poor (below -70 dBm)'] += 1
    
    signal_data = pd.DataFrame({
        'Category': list(signal_categories.keys()),
        'Count': list(signal_categories.values())
    })
    
    # Custom order for categories
    category_order = [
        'Excellent (-50 dBm or higher)',
        'Good (-60 to -51 dBm)',
        'Fair (-70 to -61 dBm)',
        'Poor (below -70 dBm)'
    ]
    
    signal_data['Category'] = pd.Categorical(
        signal_data['Category'],
        categories=category_order,
        ordered=True
    )
    
    signal_data = signal_data.sort_values('Category')
    
    # Color scale for signal quality
    domain = category_order
    range_ = ['#4CAF50', '#8BC34A', '#FFC107', '#F44336']
    
    chart = alt.Chart(signal_data).mark_bar().encode(
        x=alt.X('Count:Q', title='Number of Networks'),
        y=alt.Y('Category:N', sort=category_order, title='Signal Quality'),
        color=alt.Color('Category:N', scale=alt.Scale(domain=domain, range=range_), legend=None),
        tooltip=['Category', 'Count']
    ).properties(
        height=200
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)

def main():
    # Header
    st.markdown("""
    <div class="header">
        <h1>📶 Wi-Fi Network Scanner</h1>
        <p>Scan and analyze nearby Wi-Fi networks</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("## Controls")
        auto_refresh = st.checkbox("Auto Refresh", value=False)
        refresh_interval = st.slider("Refresh Interval (seconds)", 5, 60, 10, disabled=not auto_refresh)
        
        st.markdown("## Actions")
        scan_button = st.button("Scan Now", type="primary")
        
        st.markdown("## Notes")
        st.info("This application requires elevated privileges to scan Wi-Fi networks.")
        st.warning("Auto-refresh will continuously scan for networks, which may affect battery life.")
    
    # Initialize or retrieve networks from session state
    if 'networks' not in st.session_state:
        st.session_state.networks = []
        st.session_state.last_scan_time = None
    
    # Auto-refresh logic
    if auto_refresh and st.session_state.last_scan_time:
        current_time = time.time()
        time_diff = current_time - st.session_state.last_scan_time
        
        if time_diff >= refresh_interval:
            scan_button = True
    
    # Scan for networks when button is clicked
    if scan_button:
        with st.spinner("Scanning for Wi-Fi networks..."):
            networks = scan_wifi_networks()
            st.session_state.networks = networks
            st.session_state.last_scan_time = time.time()
    
    # Display last scan time
    if st.session_state.last_scan_time:
        scan_time = datetime.fromtimestamp(st.session_state.last_scan_time).strftime('%Y-%m-%d %H:%M:%S')
        st.markdown(f"**Last scan:** {scan_time}")
    
    # Display network information
    networks = st.session_state.networks
    
    # Display data
    create_metrics(networks)
    display_network_cards(networks)
    create_charts(networks)
    display_network_list(networks)
    
    # Auto-refresh script
    if auto_refresh:
        st.markdown("""
        <script>
            setTimeout(function(){
                window.location.reload();
            }, %s);
        </script>
        """ % (refresh_interval * 1000), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
