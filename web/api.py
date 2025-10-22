"""
Dead Simple API Server for Content Researcher Agent
Flask-based REST API
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.agent_wrapper import AgentWrapper

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# Initialize agent wrapper
agent = AgentWrapper()

@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def status():
    """Check agent status"""
    try:
        is_ready = agent.is_initialized()
        return jsonify({
            'status': 'ready' if is_ready else 'error',
            'message': 'Agent is ready' if is_ready else 'Agent initialization failed'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/research', methods=['POST'])
def research():
    """Start new research"""
    try:
        data = request.json or {}
        keywords = data.get('keywords', [])
        max_topics = data.get('max_topics', 20)
        
        result = agent.research_topics(keywords=keywords, max_topics=max_topics)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get saved topics"""
    try:
        days = int(request.args.get('days', 7))
        min_score = float(request.args.get('min_score', 60))
        
        result = agent.get_saved_topics(days=days, min_score=min_score)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics"""
    try:
        days = int(request.args.get('days', 7))
        result = agent.get_analytics(days=days)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/competitors', methods=['POST'])
def analyze_competitors():
    """Analyze competitors"""
    try:
        data = request.json
        channel_ids = data.get('channel_ids', [])
        
        if not channel_ids:
            return jsonify({'success': False, 'error': 'channel_ids required'}), 400
        
        result = agent.analyze_competitors(channel_ids)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting YouTube Content Researcher UI...")
    print("📡 Server: http://localhost:8080")
    print("🎨 Open in browser to use the UI")
    app.run(debug=True, host='127.0.0.1', port=8080)

