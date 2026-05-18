"""
Network Diagnostic Script
Checks connectivity to YouTube servers and proxy settings
"""
import sys
import os
import urllib.request
import urllib.error
import socket

def check_proxy_settings():
    print("Checking Proxy Settings...")
    print("-" * 30)
    proxies = {
        "HTTP_PROXY": os.environ.get("HTTP_PROXY"),
        "HTTPS_PROXY": os.environ.get("HTTPS_PROXY"),
        "http_proxy": os.environ.get("http_proxy"),
        "https_proxy": os.environ.get("https_proxy")
    }
    
    has_proxy = False
    for name, value in proxies.items():
        if value:
            print(f"⚠️  Found proxy variable {name}: {value}")
            has_proxy = True
    
    if not has_proxy:
        print("✅ No environment proxy variables found.")
    return has_proxy

def test_connection(url, name):
    print(f"\nTesting connection to {name} ({url})...")
    try:
        # Set a reasonable timeout
        with urllib.request.urlopen(url, timeout=10) as response:
            print(f"✅ Successfully connected to {name}")
            print(f"   Status Code: {response.getcode()}")
            return True
    except urllib.error.URLError as e:
        print(f"❌ Failed to connect to {name}")
        print(f"   Error: {e.reason}")
        if isinstance(e.reason, ConnectionRefusedError) or "10061" in str(e.reason):
            print("   🔴 CONNECTION REFUSED: This usually means a proxy is configured but not running,")
            print("      or a firewall is blocking the connection.")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False

def main():
    print("InnerTube API - Network Diagnostic Tool")
    print("=" * 50)
    
    check_proxy_settings()
    
    print("\nConnectivity Tests:")
    print("-" * 30)
    
    # Test 1: Google (General Internet)
    google_ok = test_connection("https://www.google.com", "Google")
    
    # Test 2: YouTube API (Target)
    # Note: youtubei.googleapis.com might return 404 on root, but connection should succeed
    youtube_ok = test_connection("https://youtubei.googleapis.com/generate_204", "YouTube API")
    
    print("\n" + "=" * 50)
    if google_ok and youtube_ok:
        print("🎉 Network connectivity looks good!")
        print("If the API still fails, it might be an issue with the library configuration.")
    else:
        print("⚠️  Network connectivity issues detected.")
        print("Suggestions:")
        print("1. If you have a proxy set (see above), make sure it is running.")
        print("2. Try clearing proxy environment variables if they are not needed.")
        print("3. Check your firewall or antivirus software.")
        print("4. If you are on a corporate network, you might need to configure a proxy.")

if __name__ == "__main__":
    main()
