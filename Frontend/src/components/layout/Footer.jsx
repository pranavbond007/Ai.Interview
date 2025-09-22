import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
  // Define your social media links here
  const socialLinks = [
    { name: 'GitHub', href: '#', icon: 'fab fa-github' },
    { name: 'Twitter', href: '#', icon: 'fab fa-twitter' },
    { name: 'LinkedIn', href: '#', icon: 'fab fa-linkedin-in' },
  ];

  return (
    <footer className="bg-gray-900 text-gray-400 border-t border-neon-blue/20">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Logo and Brand Section */}
          <div className="space-y-4">
            <Link to="/" className="text-2xl font-bold text-white">
              Interview<span className="text-neon-blue">AI</span>
            </Link>
            <p className="text-sm">
              Revolutionizing interview preparation with AI-powered feedback and real-time analysis.
            </p>
            <div className="flex space-x-4">
              {socialLinks.map((item) => (
                <a key={item.name} href={item.href} className="text-gray-400 hover:text-neon-blue transition-colors">
                  <span className="sr-only">{item.name}</span>
                  <i className={item.icon}></i>
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links Section */}
          <div>
            <h3 className="text-sm font-semibold text-white tracking-wider uppercase">Quick Links</h3>
            <ul className="mt-4 space-y-2">
              <li><Link to="/" className="hover:text-neon-blue">Home</Link></li>
              <li><Link to="/practice" className="hover:text-neon-blue">Practice</Link></li>
              <li><Link to="/dashboard" className="hover:text-neon-blue">Dashboard</Link></li>
              <li><Link to="/about" className="hover:text-neon-blue">About Us</Link></li>
            </ul>
          </div>

          {/* Features Section */}
          <div>
            <h3 className="text-sm font-semibold text-white tracking-wider uppercase">Features</h3>
            <ul className="mt-4 space-y-2">
              <li>Speech Analytics</li>
              <li>Performance Tracking</li>
              <li>Professional Reports</li>
              <li>Resume Parsing</li>
            </ul>
          </div>

          {/* Legal Section */}
          <div>
            <h3 className="text-sm font-semibold text-white tracking-wider uppercase">Legal</h3>
            <ul className="mt-4 space-y-2">
              <li><Link to="/privacy" className="hover:text-neon-blue">Privacy Policy</Link></li>
              <li><Link to="/terms" className="hover:text-neon-blue">Terms of Service</Link></li>
            </ul>
          </div>

        </div>
        <div className="mt-8 border-t border-gray-800 pt-8 text-center text-sm">
          <p>&copy; {new Date().getFullYear()} InterviewAI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
