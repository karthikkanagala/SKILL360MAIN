"""
UI/UX Helper Functions
Provides animated components and enhanced UI elements
"""

import streamlit as st
import time
from typing import Optional

def show_loading_animation(message: str = "Loading...", duration: float = 1.0):
    """
    Show an animated loading message
    
    Args:
        message: Loading message to display
        duration: Duration in seconds
    """
    loading_html = f"""
    <div style="text-align: center; padding: 2rem; animation: fadeIn 0.5s ease-in;">
        <div style="display: inline-block; animation: pulse 1.5s ease-in-out infinite;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <div style="font-size: 1.2rem; color: #667eea; font-weight: 600;">{message}</div>
        </div>
        <div style="margin-top: 1rem;">
            <div style="width: 200px; height: 4px; background: #e5e7eb; border-radius: 10px; margin: 0 auto; overflow: hidden;">
                <div style="width: 100%; height: 100%; background: linear-gradient(90deg, #667eea, #764ba2, #f093fb); animation: shimmer 2s infinite; background-size: 200% 100%;"></div>
            </div>
        </div>
    </div>
    """
    placeholder = st.empty()
    placeholder.markdown(loading_html, unsafe_allow_html=True)
    time.sleep(duration)
    placeholder.empty()


def show_success_animation(message: str, icon: str = "✅"):
    """
    Show animated success message
    
    Args:
        message: Success message
        icon: Icon to display
    """
    success_html = f"""
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, rgba(74, 222, 128, 0.1), rgba(34, 197, 94, 0.1)); border-radius: 16px; border-left: 4px solid #4ade80; animation: slideInRight 0.5s ease-out; margin: 1rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem; animation: bounce 0.6s ease-out;">{icon}</div>
        <div style="font-size: 1.1rem; color: #1f2937; font-weight: 600;">{message}</div>
    </div>
    """
    st.markdown(success_html, unsafe_allow_html=True)


def create_animated_card(title: str, content: str, icon: str = "📊", color: str = "#667eea"):
    """
    Create an animated card component
    
    Args:
        title: Card title
        content: Card content
        icon: Icon to display
        color: Accent color
    """
    card_html = f"""
    <div style="padding: 1.5rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05)); border-radius: 16px; border-left: 4px solid {color}; margin: 1rem 0; transition: all 0.3s ease; animation: scaleIn 0.5s ease-out;" class="hover-card">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-right: 1rem;">{icon}</div>
            <h3 style="margin: 0; font-size: 1.5rem; font-weight: 700; background: linear-gradient(135deg, {color}, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h3>
        </div>
        <div style="color: #6b7280; font-size: 1rem; line-height: 1.6;">{content}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def create_progress_ring(percentage: float, label: str, size: int = 120):
    """
    Create an animated circular progress ring
    
    Args:
        percentage: Progress percentage (0-100)
        label: Label to display
        size: Size of the ring in pixels
    """
    circumference = 2 * 3.14159 * 45  # radius = 45
    offset = circumference - (percentage / 100) * circumference
    
    ring_html = f"""
    <div style="text-align: center; animation: scaleIn 0.6s ease-out;">
        <svg width="{size}" height="{size}" style="transform: rotate(-90deg);">
            <circle cx="{size/2}" cy="{size/2}" r="45" stroke="#e5e7eb" stroke-width="8" fill="none"/>
            <circle cx="{size/2}" cy="{size/2}" r="45" stroke="url(#gradient)" stroke-width="8" fill="none"
                    stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                    style="transition: stroke-dashoffset 1s ease-out;"/>
            <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                </linearGradient>
            </defs>
        </svg>
        <div style="margin-top: -80px; font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {int(percentage)}%
        </div>
        <div style="margin-top: 40px; color: #6b7280; font-weight: 600;">{label}</div>
    </div>
    """
    st.markdown(ring_html, unsafe_allow_html=True)


def create_stat_card(value: str, label: str, icon: str, delta: Optional[str] = None, color: str = "#667eea"):
    """
    Create an enhanced stat card with animation
    
    Args:
        value: Main value to display
        label: Label for the stat
        icon: Icon emoji
        delta: Optional delta/change indicator
        color: Accent color
    """
    delta_html = f'<div style="color: {color}; font-size: 0.875rem; font-weight: 600; margin-top: 0.5rem;">↗ {delta}</div>' if delta else ''
    
    card_html = f"""
    <div style="padding: 1.5rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); border-radius: 12px; border-left: 4px solid {color}; transition: all 0.3s ease; animation: scaleIn 0.5s ease-out;" class="hover-card">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, {color}, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">
            {value}
        </div>
        <div style="color: #6b7280; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
            {label}
        </div>
        {delta_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def create_timeline_item(title: str, description: str, date: str, icon: str = "📍", is_active: bool = False):
    """
    Create a timeline item with animation
    
    Args:
        title: Item title
        description: Item description
        date: Date/time
        icon: Icon to display
        is_active: Whether this is the active/current item
    """
    border_color = "#667eea" if is_active else "#e5e7eb"
    bg_color = "rgba(102, 126, 234, 0.1)" if is_active else "rgba(249, 250, 251, 1)"
    
    timeline_html = f"""
    <div style="display: flex; margin-bottom: 1.5rem; animation: slideInLeft 0.5s ease-out;">
        <div style="flex-shrink: 0; width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; margin-right: 1rem; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);">
            {icon}
        </div>
        <div style="flex-grow: 1; padding: 1rem; background: {bg_color}; border-radius: 12px; border-left: 4px solid {border_color};">
            <div style="font-weight: 700; font-size: 1.1rem; color: #1f2937; margin-bottom: 0.25rem;">{title}</div>
            <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.5rem;">{date}</div>
            <div style="color: #4b5563; font-size: 0.95rem;">{description}</div>
        </div>
    </div>
    """
    st.markdown(timeline_html, unsafe_allow_html=True)


def create_badge(text: str, color: str = "#667eea", icon: str = ""):
    """
    Create an animated badge
    
    Args:
        text: Badge text
        color: Badge color
        icon: Optional icon
    """
    icon_html = f'<span style="margin-right: 0.25rem;">{icon}</span>' if icon else ''
    
    badge_html = f"""
    <span style="display: inline-block; padding: 0.375rem 0.875rem; border-radius: 20px; font-size: 0.875rem; font-weight: 600; background: linear-gradient(135deg, {color}, #764ba2); color: white; margin: 0.25rem; animation: scaleIn 0.3s ease-out; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        {icon_html}{text}
    </span>
    """
    st.markdown(badge_html, unsafe_allow_html=True)


def show_confetti():
    """Show confetti animation for celebrations"""
    confetti_html = """
    <script>
        // Simple confetti effect using CSS
        const colors = ['#667eea', '#764ba2', '#f093fb', '#4ade80', '#fbbf24'];
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.width = '10px';
            confetti.style.height = '10px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.top = '-10px';
            confetti.style.opacity = '1';
            confetti.style.borderRadius = '50%';
            confetti.style.animation = `fall ${2 + Math.random() * 2}s linear`;
            confetti.style.zIndex = '9999';
            document.body.appendChild(confetti);
            setTimeout(() => confetti.remove(), 4000);
        }
    </script>
    <style>
        @keyframes fall {
            to {
                transform: translateY(100vh) rotate(360deg);
                opacity: 0;
            }
        }
    </style>
    """
    st.markdown(confetti_html, unsafe_allow_html=True)
