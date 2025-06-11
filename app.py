import streamlit as st
import requests
import math
from typing import List, Dict, Any
import time

# Configure Streamlit page
st.set_page_config(
    page_title="NewsRoom",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Material Design styling
def load_css():
    st.markdown("""
    <style>
    /* Import Material Design fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    
    /* Reset and base styles */
    * {
        box-sizing: border-box;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
    }
    
    /* Enhanced smooth scrolling for the entire page */
    html {
        scroll-behavior: smooth;
        -webkit-scroll-behavior: smooth;
        -moz-scroll-behavior: smooth;
        scroll-padding-top: 20px;
    }
    
    body {
        scroll-behavior: smooth;
        -webkit-scroll-behavior: smooth;
        -moz-scroll-behavior: smooth;
        overflow-x: hidden;
        overflow-y: auto;
    }
    
    /* Enhanced smooth scrolling for Streamlit containers */
    .stApp {
        scroll-behavior: smooth;
        -webkit-scroll-behavior: smooth;
        -moz-scroll-behavior: smooth;
        scroll-padding: 20px;
        will-change: scroll-position;
    }
    
    /* Smooth scrolling momentum for mobile */
    .stApp, .main, body {
        -webkit-overflow-scrolling: touch;
        scroll-snap-type: y proximity;
    }
    
    .main {
        scroll-behavior: smooth;
        -webkit-scroll-behavior: smooth;
        -moz-scroll-behavior: smooth;
    }
    
    .main > div {
        padding-top: 2rem;
    }
    
    /* Global font family */
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Page background - Light theme */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        background-attachment: fixed;
        scroll-behavior: smooth;
        -webkit-scroll-behavior: smooth;
        -moz-scroll-behavior: smooth;
        overflow-x: hidden;
    }
    
    /* Streamlit container fixes */
    .stApp > div:first-child {
        background: transparent;
        scroll-behavior: smooth;
    }
    
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 3rem;
        padding-right: 2rem;
        max-width: 1400px;
        background: transparent;
        backdrop-filter: none;
        border-radius: 0;
        margin: 1rem auto;
        scroll-behavior: smooth;
        -webkit-scroll-behavior: smooth;
        -moz-scroll-behavior: smooth;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        margin: 0 0 2rem 0.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-weight: 500;
        font-size: 2.5rem;
        letter-spacing: -0.02em;
    }
    
    /* DISABLED - Blinking icon animation 
    .main-header h1::before {
        content: "🔴";
        display: inline-block;
        margin-right: 0.5rem;
        animation: blink 1s infinite;
        font-size: 1em;
        filter: drop-shadow(0 0 5px rgba(255, 0, 0, 0.5));
    }
    */
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
        font-weight: 300;
    }
    
    /* Card container - 2 columns layout */
    .news-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 2.5rem;
        margin: 2rem 2rem 2rem 2.5rem;
        padding: 0;
    }
    
    .news-card {
        background: white;
        border-radius: 28px;
        -webkit-border-radius: 28px;
        -moz-border-radius: 28px;
        padding: 0;
        margin: 1.5rem 0;
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.08);
        -webkit-box-shadow: 0 12px 48px rgba(0, 0, 0, 0.08);
        -moz-box-shadow: 0 12px 48px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.02);
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        -webkit-transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        -moz-transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: visible;
        display: flex;
        flex-direction: column;
        height: 600px;
        min-height: 600px;
        max-height: 600px;
        position: relative;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    
    /* Dynamic card background themes */
    .news-card.theme-blue {
        background: linear-gradient(135deg, #e3f2fd 0%, #f8fbff 100%);
        border-color: rgba(33, 150, 243, 0.1);
    }
    
    .news-card.theme-green {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        border-color: rgba(76, 175, 80, 0.1);
    }
    
    .news-card.theme-purple {
        background: linear-gradient(135deg, #f3e5f5 0%, #fce4ec 100%);
        border-color: rgba(156, 39, 176, 0.1);
    }
    
    .news-card.theme-orange {
        background: linear-gradient(135deg, #fff3e0 0%, #ffeaa7 100%);
        border-color: rgba(255, 152, 0, 0.1);
    }
    
    .news-card.theme-teal {
        background: linear-gradient(135deg, #e0f2f1 0%, #f0fdfa 100%);
        border-color: rgba(0, 150, 136, 0.1);
    }
    
    .news-card.theme-pink {
        background: linear-gradient(135deg, #fce4ec 0%, #fff0f3 100%);
        border-color: rgba(233, 30, 99, 0.1);
    }
    
    .news-card:hover {
        transform: translateY(-16px) scale(1.03);
        box-shadow: 0 32px 90px rgba(0, 0, 0, 0.15);
        border-color: rgba(102, 126, 234, 0.15);
    }
    
    .news-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #667eea 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
        z-index: 10;
    }
    
    .news-card:hover::before {
        opacity: 1;
    }
    
    .news-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0) 0%, rgba(118, 75, 162, 0.02) 100%);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .news-card:hover::after {
        opacity: 1;
    }
        opacity: 1;
    }
    
    /* Card image - Force perfect circle in all browsers */
    .news-card .card-image {
        width: 180px !important;
        height: 180px !important;
        min-width: 180px !important;
        min-height: 180px !important;
        max-width: 180px !important;
        max-height: 180px !important;
        border-radius: 50% !important;
        overflow: hidden !important;
        background: #ffffff;
        position: relative;
        margin: 0;
        border: 3px solid #ffffff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        flex-shrink: 0 !important;
        -webkit-border-radius: 50% !important;
        -moz-border-radius: 50% !important;
        -ms-border-radius: 50% !important;
        display: block !important;
    }
    
    .news-card .card-image img {
        width: 180px !important;
        height: 180px !important;
        min-width: 180px !important;
        min-height: 180px !important;
        max-width: 180px !important;
        max-height: 180px !important;
        object-fit: cover !important;
        transition: all 0.3s ease;
        filter: none !important;
        border-radius: 50% !important;
        -webkit-border-radius: 50% !important;
        -moz-border-radius: 50% !important;
        -ms-border-radius: 50% !important;
        display: block !important;
        border: none !important;
        outline: none !important;
        clip-path: circle(50% at 50% 50%) !important;
        -webkit-clip-path: circle(50% at 50% 50%) !important;
    }
    
    .news-card .card-image:hover img {
        transform: scale(1.05);
        -webkit-transform: scale(1.05);
        -moz-transform: scale(1.05);
        -ms-transform: scale(1.05);
    }
    
    /* Card content */
    .card-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1.5rem;
        background: linear-gradient(180deg, #ffffff 0%, #fafbfc 100%);
        position: relative;
    }
    
    /* Share button styling */
    .card-share {
        position: absolute;
        top: 0.75rem;
        right: 0.75rem;
        z-index: 10;
    }
    
    .share-btn {
        width: 32px;
        height: 32px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        background: rgba(102, 126, 234, 1);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .share-btn:hover {
        transform: translateY(-2px) scale(1.1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        background: rgba(102, 126, 234, 1);
    }
    
    .share-btn:active {
        transform: translateY(0) scale(0.95);
    }
    
    /* Share options dropdown */
    .share-options {
        position: absolute;
        top: 38px;
        right: 0;
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        padding: 0.5rem;
        display: none;
        min-width: 150px;
        z-index: 10;
    }
    
    .share-options.show {
        display: block;
        animation: slideDown 0.3s ease;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .share-option {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        text-decoration: none;
        color: #333;
        border-radius: 8px;
        transition: all 0.2s ease;
        font-size: 0.9rem;
        cursor: pointer;
    }
    
    .share-option:hover {
        background: #f8f9ff;
        color: #667eea;
    }
    
    .share-option-icon {
        font-size: 1.1rem;
    }
    
    /* Card header with image and title */
    .card-header {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1rem;
        position: relative;
    }
    
    /* Arrow pointing from image to text */
    .card-header::after {
        content: '→';
        position: absolute;
        left: 185px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.4rem;
        color: #667eea;
        font-weight: bold;
        animation: pointRight 2s ease-in-out infinite;
        z-index: 5;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes pointRight {
        0%, 100% { 
            transform: translateY(-50%) translateX(0px);
            opacity: 0.7;
        }
        50% { 
            transform: translateY(-50%) translateX(5px);
            opacity: 1;
        }
    }
    
    .card-header-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-left: 1.5rem;
        position: relative;
    }
    
    /* Decorative indicator for text content */
    .card-header-content::before {
        content: '';
        position: absolute;
        left: -1rem;
        top: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
        opacity: 0.6;
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a1a;
        line-height: 1.3;
        margin: 0;
        /* Full title display with proper spacing */
        word-wrap: break-word;
        hyphens: auto;
        letter-spacing: -0.01em;
        text-align: left;
    }
    
    .card-short-desc {
        color: #444;
        font-size: 0.8rem;
        line-height: 1.5;
        margin: 0;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.06) 0%, rgba(118, 75, 162, 0.06) 100%);
        border-left: 4px solid #667eea;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        font-weight: 500;
    }
    
    .card-short-desc::before {
        content: '💡';
        position: absolute;
        top: 0.75rem;
        right: 1rem;
        font-size: 0.9rem;
        opacity: 0.4;
    }
    
    .card-short-desc::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 60px;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.03));
        pointer-events: none;
    }
    
    .card-description {
        color: #555;
        font-size: 0.85rem;
        line-height: 1.6;
        margin: 0;
        text-align: left;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    
    .card-meta {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 0.75rem;
        margin-top: auto;
        padding-top: 1rem;
        flex-wrap: wrap;
        border-top: 2px solid #f8f9fa;
    }
    
    .card-source {
        background: linear-gradient(135deg, #f3e5f5 0%, #fce4ec 100%);
        color: #7b1fa2;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        border: 1px solid rgba(123, 31, 162, 0.1);
        transition: all 0.3s ease;
    }
    
    .card-source:hover {
        background: linear-gradient(135deg, #e1bee7 0%, #f8bbd9 100%);
        transform: translateY(-1px);
    }
    
    .card-date {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        color: #2e7d32;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        border: 1px solid rgba(46, 125, 50, 0.1);
        transition: all 0.3s ease;
    }
    
    .card-date:hover {
        background: linear-gradient(135deg, #c8e6c9 0%, #dcedc8 100%);
        transform: translateY(-1px);
    }
    
    .card-verification {
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        border: 1px solid;
        transition: all 0.3s ease;
    }
    
    .card-verification.verified {
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        color: #2e7d32;
        border-color: rgba(46, 125, 50, 0.1);
    }
    
    .card-verification.verified:hover {
        background: linear-gradient(135deg, #c8e6c9 0%, #dcedc8 100%);
        transform: translateY(-1px);
    }
    
    .card-verification.unverified {
        background: linear-gradient(135deg, #fff3e0 0%, #ffeaa7 100%);
        color: #f57c00;
        border-color: rgba(245, 124, 0, 0.1);
    }
    
    .card-verification.unverified:hover {
        background: linear-gradient(135deg, #ffe0b2 0%, #ffcc80 100%);
        transform: translateY(-1px);
    }
    
    .card-verification.pending {
        background: linear-gradient(135deg, #e3f2fd 0%, #e1f5fe 100%);
        color: #1976d2;
        border-color: rgba(25, 118, 210, 0.1);
    }
    
    .card-verification.pending:hover {
        background: linear-gradient(135deg, #bbdefb 0%, #b3e5fc 100%);
        transform: translateY(-1px);
    }
    
    .card-verification.unknown {
        background: linear-gradient(135deg, #f5f5f5 0%, #fafafa 100%);
        color: #666;
        border-color: rgba(102, 102, 102, 0.1);
    }
    
    .card-verification.unknown:hover {
        background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 100%);
        transform: translateY(-1px);
    }
    
    /* Card button container */
    .card-button {
        margin-top: 1.5rem;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .card-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(102, 126, 234, 0.05) 100%);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .card-button:hover::before {
        opacity: 1;
    }
    
    .card-button button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.4s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        text-transform: none;
        letter-spacing: 0.3px;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .card-button button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s ease;
    }
    
    .card-button button:hover::before {
        left: 100%;
    }
    
    .card-button button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8 0%, #6b4190 100%);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .card-button button:active {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Custom button icon animation */
    .card-button button:hover {
        animation: buttonPulse 0.6s ease-in-out;
    }
    
    @keyframes buttonPulse {
        0% { 
            transform: translateY(-4px) scale(1.02);
        }
        50% { 
            transform: translateY(-6px) scale(1.04);
        }
        100% { 
            transform: translateY(-4px) scale(1.02);
        }
    }
    
    /* Button text styling */
    .card-button button:before {
        content: '📄 ';
        font-size: 1.1rem;
        margin-right: 0.5rem;
        filter: drop-shadow(0 1px 2px rgba(0,0,0,0.1));
    }
    
    .card-button button:after {
        content: ' →';
        font-size: 1rem;
        margin-left: 0.5rem;
        transition: transform 0.3s ease;
        display: inline-block;
    }
    
    .card-button button:hover:after {
        transform: translateX(3px);
    }
    
    /* Card action box - Premium button design */
    .card-button-wrapper {
        margin-top: 1.5rem;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
        border-radius: 20px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        cursor: pointer;
    }
    
    .card-button-wrapper:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(118, 75, 162, 0.12) 100%);
        border-color: rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }
    
    .card-action-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .card-action-box:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8 0%, #6b4190 100%);
    }
    
    .action-icon {
        font-size: 1.2rem;
        filter: drop-shadow(0 1px 2px rgba(0,0,0,0.1));
        animation: iconFloat 2s ease-in-out infinite;
    }
    
    .action-text {
        font-weight: 600;
        letter-spacing: 0.3px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1));
    }
    
    .action-arrow {
        font-size: 1.1rem;
        transition: transform 0.3s ease;
        animation: arrowMove 2s ease-in-out infinite;
    }
    
    .card-action-box:hover .action-arrow {
        transform: translateX(5px);
    }
    
    @keyframes iconFloat {
        0%, 100% { 
            transform: translateY(0px);
        }
        50% { 
            transform: translateY(-2px);
        }
    }
    
    @keyframes arrowMove {
        0%, 100% { 
            transform: translateX(0px);
            opacity: 0.8;
        }
        50% { 
            transform: translateX(3px);
            opacity: 1;
        }
    }
    
    .card-button button:focus {
        outline: none;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.3);
    }
    
    /* Advertisement card styles - Same structure as news cards */
    .ad-card {
        background: white;
        border-radius: 28px;
        -webkit-border-radius: 28px;
        -moz-border-radius: 28px;
        padding: 0;
        margin: 1.5rem 0;
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.08);
        -webkit-box-shadow: 0 12px 48px rgba(0, 0, 0, 0.08);
        -moz-box-shadow: 0 12px 48px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.02);
        transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        -webkit-transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        -moz-transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        height: 600px;
        min-height: 600px;
        max-height: 600px;
        position: relative;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    
    .ad-card:hover {
        transform: translateY(-16px) scale(1.03);
        box-shadow: 0 32px 90px rgba(0, 0, 0, 0.15);
        border-color: rgba(102, 126, 234, 0.15);
    }
    
    .ad-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #e74c3c 0%, #c0392b 50%, #e74c3c 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
        z-index: 10;
    }
    
    .ad-card:hover::before {
        opacity: 1;
    }
    
    .ad-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(231, 76, 60, 0) 0%, rgba(192, 57, 43, 0.02) 100%);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.4s ease;
        z-index: 1;
    }
    
    .ad-card:hover::after {
        opacity: 1;
    }
    
    .ad-label {
        background: rgba(231, 76, 60, 0.9);
        color: white;
        padding: 0.35rem 0.75rem;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        position: absolute;
        top: 12px;
        left: 12px;
        z-index: 10;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(10px);
    }
    
    .ad-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        position: relative;
        height: 600px;
        min-height: 600px;
        max-height: 600px;
        overflow: hidden;
    }
    
    .ad-header {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1rem;
        position: relative;
    }
    
    .ad-image {
        width: 180px !important;
        height: 180px !important;
        min-width: 180px !important;
        min-height: 180px !important;
        max-width: 180px !important;
        max-height: 180px !important;
        border-radius: 50% !important;
        overflow: hidden !important;
        background: #ffffff;
        position: relative;
        margin: 0;
        border: 3px solid #ffffff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        flex-shrink: 0 !important;
        object-fit: cover !important;
        transition: all 0.3s ease;
    }
    
    .ad-header-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-left: 1.5rem;
        position: relative;
    }
    
    .ad-header-content::before {
        content: '';
        position: absolute;
        left: -1rem;
        top: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        border-radius: 2px;
        opacity: 0.6;
    }
    
    .ad-card:hover .ad-image {
        transform: scale(1.05);
        -webkit-transform: scale(1.05);
        -moz-transform: scale(1.05);
        -ms-transform: scale(1.05);
    }
    
    .ad-header::after {
        content: '💰';
        position: absolute;
        left: 185px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.4rem;
        color: #e74c3c;
        font-weight: bold;
        animation: adFloat 2s ease-in-out infinite;
        z-index: 5;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes adFloat {
        0%, 100% { 
            transform: translateY(-50%) translateX(0px);
            opacity: 0.7;
        }
        50% { 
            transform: translateY(-50%) translateX(5px);
            opacity: 1;
        }
    }
    
    .ad-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a1a;
        line-height: 1.3;
        margin: 0;
        word-wrap: break-word;
        hyphens: auto;
        letter-spacing: -0.01em;
        text-align: left;
    }
    
    .ad-short-desc {
        color: #444;
        font-size: 0.8rem;
        line-height: 1.5;
        margin: 0;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(231, 76, 60, 0.06) 0%, rgba(192, 57, 43, 0.06) 100%);
        border-left: 4px solid #e74c3c;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        font-weight: 500;
    }
    
    .ad-short-desc::before {
        content: '💡';
        position: absolute;
        top: 0.75rem;
        right: 1rem;
        font-size: 0.9rem;
        opacity: 0.4;
    }
    
    .ad-description {
        color: #555;
        font-size: 0.85rem;
        line-height: 1.6;
        margin: 0;
        text-align: left;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    
    .ad-meta {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 0.75rem;
        margin-top: auto;
        padding-top: 1rem;
        flex-wrap: wrap;
        border-top: 2px solid #f8f9fa;
    }
    
    .ad-category {
        background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
        color: #e74c3c;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        border: 1px solid rgba(231, 76, 60, 0.1);
        transition: all 0.3s ease;
    }
    
    .ad-category:hover {
        background: linear-gradient(135deg, #ffcdd2 0%, #f8bbd9 100%);
        transform: translateY(-1px);
    }
    
    .ad-button-wrapper {
        margin-top: 1.5rem;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(231, 76, 60, 0.08) 0%, rgba(192, 57, 43, 0.08) 100%);
        border-radius: 20px;
        border: 2px solid rgba(231, 76, 60, 0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        cursor: pointer;
    }
    
    .ad-button-wrapper:hover {
        background: linear-gradient(135deg, rgba(231, 76, 60, 0.12) 0%, rgba(192, 57, 43, 0.12) 100%);
        border-color: rgba(231, 76, 60, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(231, 76, 60, 0.15);
    }
    
    .ad-action-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        border-radius: 16px;
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .ad-action-box:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(231, 76, 60, 0.4);
        background: linear-gradient(135deg, #dc3545 0%, #a71e2a 100%);
    }
    
    /* Pagination */
    .pagination-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin: 2rem 2rem 2rem 2.5rem;
        padding: 1.5rem;
        background: transparent;
        border-radius: 16px;
        box-shadow: none;
    }
    
    .pagination-info {
        color: #666;
        font-size: 0.9rem;
        margin: 0 1rem;
        text-align: center;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: 500;
    }
    
    /* Pagination button alignment */
    .pagination-container [data-testid="column"]:first-child {
        display: flex;
        justify-content: flex-start;
        align-items: center;
    }
    
    .pagination-container [data-testid="column"]:nth-child(2) {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .pagination-container [data-testid="column"]:last-child {
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    
    /* Enhanced pagination button styling */
    .pagination-container [data-testid="stButton"] > button {
        min-width: 120px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border-radius: 12px;
        border: 2px solid #667eea;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .pagination-container [data-testid="stButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Page number buttons styling */
    .page-numbers-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .page-numbers-row [data-testid="stButton"] > button {
        min-width: 40px;
        width: 40px;
        height: 40px;
        padding: 0;
        font-weight: 500;
        border-radius: 50%;
        border: 1px solid #e0e0e0;
        background: white;
        color: #666;
        transition: all 0.2s ease;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 0.9rem;
    }
    
    .page-numbers-row [data-testid="stButton"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        background: #f8f9ff;
        border-color: #667eea;
        color: #667eea;
    }
    
    /* Active page button */
    .page-numbers-row .active-page [data-testid="stButton"] > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        font-weight: 600;
    }
    
    .page-numbers-row .active-page [data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        transform: none;
    }
    
    /* Ellipsis styling */
    .page-ellipsis {
        color: #999;
        font-weight: 500;
        padding: 0 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 40px;
        font-size: 1.2rem;
    }
    
    /* Loading animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Error styling */
    .error-container {
        background: #ffebee;
        border: 1px solid #ffcdd2;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: #c62828;
    }
    
    /* Smooth scroll animations and viewport optimizations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* News card entrance animation */
    .news-card {
        animation: fadeInUp 0.6s ease-out;
        will-change: transform, opacity;
        scroll-snap-align: start;
    }
    
    /* Staggered animation delay for cards */
    .news-card:nth-child(1) { animation-delay: 0s; }
    .news-card:nth-child(2) { animation-delay: 0.1s; }
    .news-card:nth-child(3) { animation-delay: 0.2s; }
    .news-card:nth-child(4) { animation-delay: 0.3s; }
    .news-card:nth-child(5) { animation-delay: 0.4s; }
    .news-card:nth-child(6) { animation-delay: 0.5s; }
    
    /* Load more button smooth animation */
    #load-more-btn {
        animation: slideIn 0.5s ease-out;
        will-change: transform, opacity;
    }
    
    #load-more-btn:hover {
        transform: translateY(-2px) scale(1.05);
    }
    
    #load-more-btn:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Smooth transitions for all interactive elements */
    * {
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    </style>
    """, unsafe_allow_html=True)

def fetch_news_data() -> List[Dict[str, Any]]:
    """Fetch news data from the API without caching."""
    try:
        response = requests.get("https://349z5cfhwi.execute-api.us-west-2.amazonaws.com/default/news_feed", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract stories from the API response
        if isinstance(data, dict) and 'stories' in data:
            return data['stories']
        elif isinstance(data, list):
            return data
        else:
            st.error("Unexpected API response format")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return []

def fetch_article_detail() -> Dict[str, Any]:
    """Fetch detailed article data from the fixed detail API for all articles."""
    try:
        response = requests.get("https://api.npoint.io/d94fa493a4bcd7394480", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract story from the API response
        if isinstance(data, dict) and 'story' in data:
            return data['story']
        else:
            st.error("Unexpected detail API response format")
            return {}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching article details: {str(e)}")
        return {}

def render_article_detail(article_data: Dict[str, Any]) -> None:
    """Render detailed article view."""
    
    # Back button
    if st.button("← Back to News List", key="back_btn", help="Return to news list"):
        st.session_state.selected_article_id = None
        st.query_params.clear()
        st.rerun()
    
    # Article image
    image_url = article_data.get('image', '')
    if image_url:
        st.image(image_url, use_container_width=True, caption=article_data.get('title', 'Article Image'))
    
    # Article title
    st.markdown(f"# {article_data.get('title', 'No Title')}")
    
    # Meta information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if article_data.get('source'):
            st.markdown(f"**Source:** {article_data['source']}")
    
    with col2:
        if article_data.get('published_date'):
            try:
                from datetime import datetime
                date_obj = datetime.fromisoformat(article_data['published_date'].replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%B %d, %Y at %I:%M %p')
                st.markdown(f"**Published:** {formatted_date}")
            except:
                st.markdown(f"**Published:** {article_data['published_date']}")
    
    with col3:
        if article_data.get('verification_status'):
            status = article_data['verification_status']
            icon = get_verification_icon(status)
            st.markdown(f"**Status:** {icon} {status.title()}")
    
    st.markdown("---")
    
    # Short description (summary)
    if article_data.get('short_description'):
        import re
        short_desc = article_data['short_description']
        
        # Better HTML handling for short description
        short_desc = re.sub(r'<br\s*/?>', ' ', short_desc)     # Convert breaks to spaces
        short_desc = re.sub(r'<p>', ' ', short_desc)           # Convert paragraphs to spaces  
        short_desc = re.sub(r'</p>', ' ', short_desc)
        short_desc = re.sub(r'<strong>(.*?)</strong>', r'**\1**', short_desc)  # Bold
        short_desc = re.sub(r'<b>(.*?)</b>', r'**\1**', short_desc)            # Bold
        short_desc = re.sub(r'<em>(.*?)</em>', r'*\1*', short_desc)            # Italic
        short_desc = re.sub(r'<i>(.*?)</i>', r'*\1*', short_desc)              # Italic
        short_desc = re.sub(r'<[^<]+?>', '', short_desc)                        # Remove remaining tags
        short_desc = ' '.join(short_desc.split())                               # Clean whitespace
        
        st.markdown("### 📝 Summary")
        st.info(short_desc)
    
    # Add advertisement in detail view
    st.markdown("---")
    ad_col1, ad_col2, ad_col3 = st.columns([1, 2, 1])
    with ad_col2:
        render_ad_card(f"detail_ad_{article_data.get('id', 'unknown')}")
    st.markdown("---")
    
    # Full article content
    if article_data.get('long_description'):
        long_desc = article_data['long_description']
        
        # Clean up and preserve basic HTML formatting
        import re
        # Keep basic formatting tags and convert to markdown-friendly format
        long_desc = re.sub(r'<br\s*/?>', '\n\n', long_desc)  # Convert breaks to paragraphs
        long_desc = re.sub(r'<p>', '\n\n', long_desc)        # Convert paragraphs
        long_desc = re.sub(r'</p>', '', long_desc)
        long_desc = re.sub(r'<strong>(.*?)</strong>', r'**\1**', long_desc)  # Bold
        long_desc = re.sub(r'<b>(.*?)</b>', r'**\1**', long_desc)            # Bold
        long_desc = re.sub(r'<em>(.*?)</em>', r'*\1*', long_desc)            # Italic
        long_desc = re.sub(r'<i>(.*?)</i>', r'*\1*', long_desc)              # Italic
        long_desc = re.sub(r'<[^<]+?>', '', long_desc)                        # Remove remaining tags
        long_desc = ' '.join(long_desc.split())                               # Clean whitespace
        
        st.markdown("### 📄 Full Article")
        st.markdown(long_desc)
    
    # Original link
    if article_data.get('original_link'):
        st.markdown("---")
        st.markdown(f"[🔗 Read Original Article]({article_data['original_link']})")

def get_verification_icon(status: str) -> str:
    """Get the appropriate icon for verification status."""
    status_lower = status.lower()
    if status_lower == 'verified':
        return '✅'
    elif status_lower == 'unverified':
        return '⚠️'
    elif status_lower == 'pending':
        return '⏳'
    else:
        return '❓'

def render_ad_card(ad_position: str) -> None:
    """Render an advertisement card with enhanced visual design."""
    
    # Premium ad designs with better visuals and varied themes
    ad_designs = [
        {
            "image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=260&fit=crop&crop=center",
            "title": "🚀 Launch Your Business",
            "description": "Transform your ideas into reality with our premium business solutions.",
            "button": "Get Started",
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        },
        {
            "image": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=400&h=260&fit=crop&crop=center",
            "title": "📊 Analytics Pro",
            "description": "Unlock powerful insights with advanced data analytics and reporting tools.",
            "button": "Try Free",
            "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
        },
        {
            "image": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=400&h=260&fit=crop&crop=center",
            "title": "🎯 Marketing Suite",
            "description": "Boost your reach with AI-powered marketing automation and targeting.",
            "button": "Learn More",
            "gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
        },
        {
            "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=260&fit=crop&crop=center",
            "title": "💼 Business Elite",
            "description": "Premium tools and services designed for growing businesses.",
            "button": "Upgrade Now",
            "gradient": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
        },
        {
            "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=260&fit=crop&crop=center",
            "title": "⭐ Premium Plus",
            "description": "Experience the ultimate in productivity with our flagship solution.",
            "button": "Subscribe",
            "gradient": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)"
        },
        {
            "image": "https://images.unsplash.com/photo-1553484771-371a605b060b?w=400&h=260&fit=crop&crop=center",
            "title": "🔒 Security First",
            "description": "Protect your business with enterprise-grade security solutions.",
            "button": "Secure Now",
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        },
        {
            "image": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=400&h=260&fit=crop&crop=center",
            "title": "💰 Finance Pro",
            "description": "Smart financial management tools for modern businesses.",
            "button": "Start Free",
            "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        },
        {
            "image": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=400&h=260&fit=crop&crop=center",
            "title": "🎨 Creative Suite",
            "description": "Professional design tools for creators and agencies.",
            "button": "Explore",
            "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
        },
        {
            "image": "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400&h=260&fit=crop&crop=center",
            "title": "📱 Mobile First",
            "description": "Build amazing mobile apps with our development platform.",
            "button": "Build Now",
            "gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
        }
    ]
    
    # Select ad design based on position - simple index approach
    # Extract number from ad_position string like "list_ad_3"
    try:
        ad_num = int(ad_position.split('_')[-1])
        ad_index = ad_num % len(ad_designs)
    except:
        # Fallback to hash if parsing fails
        import hashlib
        position_hash = int(hashlib.md5(ad_position.encode()).hexdigest(), 16)
        ad_index = position_hash % len(ad_designs)
    
    ad_data = ad_designs[ad_index]
    
    ad_html = f"""
    <div class="ad-card">
        <div class="ad-label">Advertisement</div>
        <div class="ad-content" style="padding: 0; height: 600px;">
            <img src="{ad_data['image']}" alt="Advertisement" 
                 style="width: 100%; height: 600px; object-fit: cover; border-radius: 0 0 24px 24px;"
                 onerror="this.src='https://via.placeholder.com/400x600/e74c3c/ffffff?text=Premium+Ad'">
            <div style="position: absolute; bottom: 20px; left: 20px; right: 20px; background: rgba(0,0,0,0.8); color: white; padding: 15px; border-radius: 12px; text-align: center; backdrop-filter: blur(10px);">
                <h3 style="margin: 0 0 10px 0; font-size: 1.1rem; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">{ad_data['title']}</h3>
                <button style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; border: none; padding: 10px 20px; border-radius: 25px; font-size: 0.85rem; font-weight: 600; cursor: pointer; box-shadow: 0 4px 15px rgba(231,76,60,0.3); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(231,76,60,0.4)'" onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 4px 15px rgba(231,76,60,0.3)'">{ad_data['button']} →</button>
            </div>
        </div>
    </div>
    """
    
    st.markdown(ad_html, unsafe_allow_html=True)

def render_news_card(news_item: Dict[str, Any], col) -> None:
    """Render a single news card with Material Design styling."""
    
    with col:
        # Handle missing image
        image_url = news_item.get('image', '')
        if not image_url or image_url == "":
            image_url = "https://via.placeholder.com/120x120/667eea/ffffff?text=📰"
        
        # Clean up the short description (remove HTML tags)
        import re
        short_description = news_item.get('short_description', '')
        if short_description:
            short_description = re.sub('<[^<]+?>', '', short_description)
            short_description = ' '.join(short_description.split())
        
        # Clean up the long description (remove HTML tags) 
        long_description = news_item.get('long_description', '')
        if long_description:
            long_description = re.sub('<[^<]+?>', '', long_description)
            long_description = ' '.join(long_description.split())
        
        # Use long description if available, otherwise short description
        full_description = long_description if long_description else short_description
        if not full_description:
            full_description = 'No description available.'
        
        # Format published date
        published_date = news_item.get('published_date', '')
        formatted_date = ''
        if published_date:
            try:
                from datetime import datetime
                # Parse the ISO date string
                date_obj = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%B %d, %Y')
            except:
                formatted_date = published_date
        
        # Create card with dynamic theme
        article_id = news_item.get('id', 0)
        
        # Dynamic theme selection based on article ID
        themes = ['theme-blue', 'theme-green', 'theme-purple', 'theme-orange', 'theme-teal', 'theme-pink']
        theme_class = themes[article_id % len(themes)]
        
        # Create simplified share functionality with proper URLs
        # Get current page URL and unique card ID
        app_url = "https://newsroom.streamlit.app"
        article_url = f"{app_url}?article={article_id}"  # Specific article URL
        card_id = f"card_{article_id}"
        title = news_item.get('title', 'Check out this news').replace("'", "\\'")  # Escape quotes
        encoded_title = requests.utils.quote(title)  # URL encode title
        
        # Use Unicode share icon
        share_icon = "⤴"  # Share/upload icon
        
        card_html = f"""
        <div class="news-card {theme_class}">
            <div class="card-share">
                <div class="share-btn" onclick="toggleShare{card_id}()" title="Share">
                    {share_icon}
                </div>
                <div class="share-options" id="share-options-{card_id}">
                    <div class="share-option" onclick="shareToFacebook{card_id}()">
                        <span class="share-option-icon">📘</span>
                        <span>Facebook</span>
                    </div>
                    <div class="share-option" onclick="shareToTwitter{card_id}()">
                        <span class="share-option-icon">🐦</span>
                        <span>Twitter</span>
                    </div>
                    <div class="share-option" onclick="shareToWhatsApp{card_id}()">
                        <span class="share-option-icon">💬</span>
                        <span>WhatsApp</span>
                    </div>
                    <div class="share-option" onclick="shareToEmail{card_id}()">
                        <span class="share-option-icon">📧</span>
                        <span>Email</span>
                    </div>
                    <div class="share-option" onclick="copyLink{card_id}()">
                        <span class="share-option-icon">📋</span>
                        <span>Copy Link</span>
                    </div>
                </div>
            </div>
            <div class="card-content">
                <div class="card-header">
                    <div class="card-image">
                        <img src="{image_url}" alt="News image" onerror="this.src='https://via.placeholder.com/120x120/667eea/ffffff?text=📰'">
                    </div>
                    <div class="card-header-content">
                        <h3 class="card-title">{news_item.get('title', 'No Title')}</h3>
                    </div>
                </div>
                {f'<div class="card-short-desc"><strong>Summary:</strong> {short_description}</div>' if short_description else ''}
                <p class="card-description">{full_description}</p>
                <div class="card-meta">
                    <span class="card-source">{news_item.get('source', 'Unknown')}</span>
                    {f'<span class="card-date">📅 {formatted_date}</span>' if formatted_date else ''}
                    <span class="card-verification {news_item.get('verification_status', 'unknown').lower()}">{get_verification_icon(news_item.get('verification_status', 'unknown'))} {news_item.get('verification_status', 'Unknown').title()}</span>
                </div>
                <div class="card-button-wrapper">
                    <a href="?showdetail=1" style="text-decoration: none; color: inherit;">
                        <div class="card-action-box">
                            <div class="action-icon">📖</div>
                            <div class="action-text">Read More</div>
                            <div class="action-arrow">→</div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
        
        <script>
        function toggleShare{card_id}() {{
            // Try Web Share API first (mobile/modern browsers)
            if (navigator.share) {{
                navigator.share({{
                    title: '{title}',
                    text: 'Check out this news story: {title}',
                    url: '{article_url}'
                }}).then(() => {{
                    showShareSuccess{card_id}();
                }}).catch((error) => {{
                    console.log('Error sharing:', error);
                    showShareMenu{card_id}();

                }});
            }} else {{
                // Fallback to custom share menu
                showShareMenu{card_id}();
            }}
        }}
        
        function showShareMenu{card_id}() {{
            const shareOptions = document.getElementById('share-options-{card_id}');
            const shareBtn = shareOptions.previousElementSibling;
            const isVisible = shareOptions.classList.contains('show');
            
            // Hide all other share menus
            document.querySelectorAll('.share-options').forEach(menu => {{
                menu.classList.remove('show');
            }});
            
            // Reset all share buttons
            document.querySelectorAll('.share-btn').forEach(btn => {{
                btn.innerHTML = '⤴';
            }});
            
            // Toggle current menu
            if (!isVisible) {{
                shareOptions.classList.add('show');
                shareBtn.innerHTML = '✕'; // Change to close icon when open
            }}
        }}
        
        function shareToFacebook{card_id}() {{
            const url = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent('{article_url}');
            window.open(url, '_blank', 'width=600,height=400');
            hideShareMenu{card_id}();
            showShareSuccess{card_id}();
        }}
        
        function shareToTwitter{card_id}() {{
            const text = 'Check out this news: {title}';
            const url = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(text) + '&url=' + encodeURIComponent('{article_url}');
            window.open(url, '_blank', 'width=600,height=400');
            hideShareMenu{card_id}();
            showShareSuccess{card_id}();
        }}
        
        function shareToWhatsApp{card_id}() {{
            const text = 'Check out this news: {title} - {article_url}';
            const url = 'https://wa.me/?text=' + encodeURIComponent(text);
            window.open(url, '_blank');
            hideShareMenu{card_id}();
            showShareSuccess{card_id}();
        }}
        
        function shareToEmail{card_id}() {{
            const subject = encodeURIComponent('{title}');
            const body = encodeURIComponent('Check out this interesting news story:\\n\\n{title}\\n\\nRead more: {article_url}');
            const url = 'mailto:?subject=' + subject + '&body=' + body;
            window.location.href = url;
            hideShareMenu{card_id}();
            showShareSuccess{card_id}();
        }}
        
        function hideShareMenu{card_id}() {{
            document.getElementById('share-options-{card_id}').classList.remove('show');
            document.querySelector('#share-options-{card_id}').previousElementSibling.innerHTML = '⤴';
        }}
            const shareBtn = document.querySelector('#share-options-{card_id}').previousElementSibling;
            shareBtn.innerHTML = '♥';
            shareBtn.style.background = '#4CAF50';
            
            setTimeout(() => {{
                shareBtn.innerHTML = '⤴';
                shareBtn.style.background = 'rgba(102, 126, 234, 1)';
            }}, 2000);
        }}
        
        function copyLink{card_id}() {{
            const url = '{article_url}';
            const title = '{title}';
            const textToCopy = `${{title}}\\n\\nRead more: ${{url}}`;
            
            if (navigator.clipboard) {{
                navigator.clipboard.writeText(textToCopy).then(function() {{
                    hideShareMenu{card_id}();
                    showCopySuccess{card_id}();
                }}).catch(function() {{
                    fallbackCopy{card_id}(textToCopy);
                }});
            }} else {{
                fallbackCopy{card_id}(textToCopy);
            }}
        }}
        
        function fallbackCopy{card_id}(text) {{
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            hideShareMenu{card_id}();
            showCopySuccess{card_id}();
        }}
        
        function showCopySuccess{card_id}() {{
            const shareBtn = document.querySelector('#share-options-{card_id}').previousElementSibling;
            shareBtn.innerHTML = '♥';
            shareBtn.style.background = '#4CAF50';
            
            setTimeout(() => {{
                shareBtn.innerHTML = '⤴';
                shareBtn.style.background = 'rgba(102, 126, 234, 1)';
            }}, 2000);
        }}
        
        function trackShare(platform, articleId) {{
            // Track share analytics (optional)
            console.log(`Shared article ${{articleId}} on ${{platform}}`);
        }}
        
        // Close share menus when clicking outside
        document.addEventListener('click', function(event) {{
            if (!event.target.closest('.card-share')) {{
                document.querySelectorAll('.share-options').forEach(menu => {{
                    menu.classList.remove('show');
                }});
                document.querySelectorAll('.share-btn').forEach(btn => {{
                    btn.innerHTML = '⤴';
                }});
            }}
        }});
        </script>
        """

        
        st.markdown(card_html, unsafe_allow_html=True)
        

def render_pagination(current_page: int, total_pages: int, total_items: int, items_per_page: int, position: str = "top") -> None:
    """Render advanced pagination controls with ellipsis style like professional websites."""
    
    start_item = (current_page - 1) * items_per_page + 1
    end_item = min(current_page * items_per_page, total_items)
    
    # Create the pagination layout
    col1, col2, col3 = st.columns([1,  3, 1])
    
    # Previous button
    with col1:
        if current_page > 1:
            if st.button("← Previous", key=f"prev_btn_{position}", help="Go to previous page"):
                st.session_state.current_page = current_page - 1
                st.rerun()
    
    # Page numbers with ellipsis and info
    with col2:
        # Info text
        pagination_info = f"""
        <div class="pagination-info">
            Showing {start_item}-{end_item} of {total_items} items (Page {current_page} of {total_pages})
        </div>
        """
        st.markdown(pagination_info, unsafe_allow_html=True)
        
        # Only show page numbers if we have more than 1 page
        if total_pages > 1:
            # Generate page numbers with ellipsis logic
            page_numbers = get_page_numbers_with_ellipsis(current_page, total_pages)
            
            # Create dynamic columns for page numbers
            if len(page_numbers) > 0:
                st.markdown('<div class="page-numbers-row">', unsafe_allow_html=True)
                
                # Create columns for page numbers
                page_cols = st.columns(len(page_numbers))
                
                for i, page_item in enumerate(page_numbers):
                    with page_cols[i]:
                        if page_item == "...":
                            # Ellipsis
                            st.markdown('<div class="page-ellipsis">...</div>', unsafe_allow_html=True)
                        elif page_item == current_page:
                            # Active page (non-clickable)
                            st.markdown(f'<div class="active-page">', unsafe_allow_html=True)
                            st.button(f"{page_item}", key=f"active_page_{page_item}_{position}", disabled=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            # Clickable page number
                            if st.button(f"{page_item}", key=f"page_{page_item}_{position}", help=f"Go to page {page_item}"):
                                st.session_state.current_page = page_item
                                st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Next button
    with col3:
        if current_page < total_pages:
            st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
            if st.button("Next →", key=f"next_btn_{position}", help="Go to next page"):
                st.session_state.current_page = current_page + 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


def get_page_numbers_with_ellipsis(current_page: int, total_pages: int, max_visible: int = 7) -> List:
    """
    Generate page numbers with ellipsis for pagination.
    Shows first page, last page, current page and surrounding pages, with ellipsis where needed.
    
    Args:
        current_page: Current active page
        total_pages: Total number of pages
        max_visible: Maximum number of visible page buttons (excluding ellipsis)
    
    Returns:
        List of page numbers and ellipsis ("...") to display
    """
    if total_pages <= max_visible:
        # If total pages is small, show all pages
        return list(range(1, total_pages + 1))
    
    # Always show first and last page
    pages = []
    
    # Determine the range around current page
    half_range = (max_visible - 4) // 2  # Reserve space for first, last, and ellipsis
    start_range = max(2, current_page - half_range)
    end_range = min(total_pages - 1, current_page + half_range)
    
    # Add first page
    pages.append(1)
    
    # Add ellipsis after first page if needed
    if start_range > 2:
        pages.append("...")
    
    # Add pages around current page
    for page in range(start_range, end_range + 1):
        if page != 1 and page != total_pages:  # Don't duplicate first/last
            pages.append(page)
    
    # Add ellipsis before last page if needed
    if end_range < total_pages - 1:
        pages.append("...")
    
    # Add last page (if not already included)
    if total_pages > 1:
        pages.append(total_pages)
    
    return pages

def main():
    """Main application function."""
    
    # Load custom CSS
    load_css()
    
    # Header
    header_html = """
    <div class="main-header">
        <h1>📰 NewsRoom</h1>
        <p>Stay updated with the latest news and stories</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    if 'selected_article_id' not in st.session_state:
        st.session_state.selected_article_id = None
    
    # Check URL parameter for detail page (only if not already showing detail)
    if 'showdetail' in st.query_params and st.session_state.selected_article_id is None:
        st.session_state.selected_article_id = 1  # Any ID works since we use same content
    
    # Check if we should show article detail
    if st.session_state.selected_article_id is not None:
        with st.spinner("Loading article details..."):
            article_detail = fetch_article_detail()
        
        if article_detail:
            render_article_detail(article_detail)
        else:
            st.error("Unable to load article details.")
            if st.button("← Back to News List"):
                st.session_state.selected_article_id = None
                st.query_params.clear()
                st.rerun()
        return
    
    # Configuration for infinite scroll
    ITEMS_PER_LOAD = 12  # Load 12 items at a time (4 rows of 3)
    
    # Initialize session state for infinite scroll
    if 'loaded_items' not in st.session_state:
        st.session_state.loaded_items = ITEMS_PER_LOAD
    
    # Fetch data
    with st.spinner("Loading news..."):
        news_data = fetch_news_data()
    
    if not news_data:
        error_html = """
        <div class="error-container">
            <h3>⚠️ Unable to load news</h3>
            <p>Please check your internet connection and try again.</p>
        </div>
        """
        st.markdown(error_html, unsafe_allow_html=True)
        return
    
    # Get items to display (based on loaded_items count)
    total_items = len(news_data)
    items_to_show = min(st.session_state.loaded_items, total_items)
    current_items = news_data[:items_to_show]

    # Render news cards in 3-column grid with ads
    items_with_ads = []
    
    # Insert ads between news items
    for i, item in enumerate(current_items):
        items_with_ads.append(('news', item))
        # Add ad after every 3rd article (positions 3, 6, 9)
        if (i + 1) % 3 == 0 and i < len(current_items) - 1:
            items_with_ads.append(('ad', f"list_ad_{i}"))
    
    # Add one more ad at the end (last row)
    items_with_ads.append(('ad', f"list_ad_end"))
    
    # Render items in 3-column grid
    for i in range(0, len(items_with_ads), 3):
        cols = st.columns(3, gap="large")
        for j, col in enumerate(cols):
            if i + j < len(items_with_ads):
                item_type, item_data = items_with_ads[i + j]
                if item_type == 'news':
                    render_news_card(item_data, col)
                else:  # ad
                    with col:
                        render_ad_card(item_data)
    
    # Infinite scroll - Load more button
    if items_to_show < total_items:
        st.markdown('<div style="text-align: center; margin: 3rem 0 2rem 0;">', unsafe_allow_html=True)
        
        # Auto-load more content with JavaScript
        load_more_html = f"""
        <div id="load-more-container" style="text-align: center; padding: 2rem 0; margin: 1rem 0;">
            <button id="load-more-btn" onclick="loadMore()" 
                    style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           color: white; border: none; padding: 12px 24px; 
                           border-radius: 25px; cursor: pointer; font-size: 16px;
                           box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                           transition: all 0.3s ease;
                           margin-bottom: 1rem;">
                📰 Load More News ({total_items - items_to_show} remaining)
            </button>
        </div>
        
        <script>
        let isLoading = false;
        let ticking = false;
        
        function loadMore() {{
            if (isLoading) return;
            isLoading = true;
            
            // Add loading animation
            const btn = document.getElementById('load-more-btn');
            if (btn) {{
                btn.innerHTML = '⏳ Loading...';
                btn.style.opacity = '0.7';
            }}
            
            // Smooth scroll to current position before reload
            const currentScroll = window.scrollY;
            sessionStorage.setItem('scrollPosition', currentScroll);
            
            // Trigger Streamlit rerun to load more items
            window.parent.document.querySelector('[data-testid="stAppViewContainer"]').dispatchEvent(
                new CustomEvent('loadmore', {{ detail: {{ action: 'loadmore' }} }})
            );
        }}
        
        // Throttled scroll handler for better performance
        function handleScroll() {{
            if (!ticking) {{
                requestAnimationFrame(function() {{
                    const scrollPosition = window.innerHeight + window.scrollY;
                    const documentHeight = document.body.offsetHeight;
                    const threshold = documentHeight - 800; // Trigger earlier
                    
                    if (scrollPosition >= threshold && !isLoading) {{
                        const btn = document.getElementById('load-more-btn');
                        if (btn && btn.style.display !== 'none') {{
                            // Smooth loading transition
                            btn.style.transform = 'scale(0.95)';
                            setTimeout(() => {{
                                btn.click();
                                btn.style.display = 'none';
                            }}, 200);
                        }}
                    }}
                    ticking = false;
                }});
                ticking = true;
            }}
        }}
        
        // Enhanced scroll listener with passive option for better performance
        window.addEventListener('scroll', handleScroll, {{ passive: true }});
        
        // Restore scroll position after load
        window.addEventListener('load', function() {{
            const savedPosition = sessionStorage.getItem('scrollPosition');
            if (savedPosition) {{
                window.scrollTo({{
                    top: parseInt(savedPosition),
                    behavior: 'smooth'
                }});
                sessionStorage.removeItem('scrollPosition');
            }}
        }});
        
        // Smooth scroll to new content after load
        setTimeout(() => {{
            if (window.scrollY > 0) {{
                window.scrollTo({{
                    top: window.scrollY + 100,
                    behavior: 'smooth'
                }});
            }}
        }}, 500);
        </script>
        """
        st.markdown(load_more_html, unsafe_allow_html=True)
        
        # Manual load more button with proper spacing
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📰 Load More News", key="load_more", help=f"{total_items - items_to_show} more stories available"):
                st.session_state.loaded_items += ITEMS_PER_LOAD
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)  # Extra spacing
    else:
        # End of content indicator with proper spacing
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align: center; padding: 2rem; color: #666; margin: 2rem 0; '
            'background: rgba(255,255,255,0.5); border-radius: 15px; backdrop-filter: blur(10px);">'
            '🎉 You\'ve reached the end! All news stories loaded.'
            '</div>', 
            unsafe_allow_html=True
        )
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)  # Extra spacing
    
    # Footer with proper spacing
    st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)  # Spacer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 2rem; margin: 1rem 0; "
        "background: rgba(255,255,255,0.8); border-radius: 15px; backdrop-filter: blur(10px);'>"
        "Built with ❤️ using Streamlit and Material Design"
        "</div>", 
        unsafe_allow_html=True
    )
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)  # Bottom spacer

if __name__ == "__main__":
    main()
