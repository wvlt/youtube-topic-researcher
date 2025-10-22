// YouTube Content Researcher - Frontend

const API_BASE = '';

// State
let currentTopics = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkStatus();
    loadTopics();
    loadAnalytics();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Start Research
    document.getElementById('start-research-btn').addEventListener('click', startResearch);
    
    // Refresh
    document.getElementById('refresh-btn').addEventListener('click', loadTopics);
    
    // Filter changes
    document.getElementById('filter-days').addEventListener('change', loadTopics);
    document.getElementById('min-score').addEventListener('change', loadTopics);
    document.getElementById('favorites-only').addEventListener('change', loadTopics);
    
    // Modal close
    document.querySelector('.close').addEventListener('click', closeModal);
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('topic-modal');
        if (e.target === modal) {
            closeModal();
        }
    });
}

// Check Agent Status
async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        const data = await response.json();
        
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        
        if (data.status === 'ready') {
            statusDot.className = 'status-dot ready';
            statusText.textContent = 'Ready';
        } else {
            statusDot.className = 'status-dot error';
            statusText.textContent = 'Error';
        }
    } catch (error) {
        console.error('Status check failed:', error);
        document.getElementById('status-dot').className = 'status-dot error';
        document.getElementById('status-text').textContent = 'Offline';
    }
}

// Start Research
async function startResearch() {
    const keywordsInput = document.getElementById('keywords-input').value;
    const maxTopics = parseInt(document.getElementById('max-topics-input').value);
    const btn = document.getElementById('start-research-btn');
    const statusMsg = document.getElementById('research-status');
    
    // Parse keywords
    const keywords = keywordsInput
        .split(',')
        .map(k => k.trim())
        .filter(k => k.length > 0);
    
    // Disable button
    btn.disabled = true;
    btn.textContent = '🔄 Researching...';
    
    // Show loading status
    statusMsg.className = 'status-message loading show';
    statusMsg.textContent = '🔍 Researching topics... This may take a few minutes.';
    
    try {
        const response = await fetch(`${API_BASE}/api/research`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keywords: keywords.length > 0 ? keywords : null,
                max_topics: maxTopics
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            statusMsg.className = 'status-message success show';
            statusMsg.textContent = `✅ Found ${data.count} topics!`;
            
            // Refresh data
            await loadTopics();
            await loadAnalytics();
        } else {
            throw new Error(data.error || 'Research failed');
        }
    } catch (error) {
        console.error('Research failed:', error);
        statusMsg.className = 'status-message error show';
        statusMsg.textContent = `❌ Error: ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = '🚀 Start Research';
        
        // Hide status after 5 seconds
        setTimeout(() => {
            statusMsg.classList.remove('show');
        }, 5000);
    }
}

// Load Topics
async function loadTopics() {
    const days = document.getElementById('filter-days').value;
    const minScore = document.getElementById('min-score').value;
    const favoritesOnly = document.getElementById('favorites-only').checked;
    const container = document.getElementById('results-container');
    
    // Show loading
    container.innerHTML = '<div class="spinner"></div>';
    
    try {
        const response = await fetch(`${API_BASE}/api/topics?days=${days}&min_score=${minScore}&favorited_only=${favoritesOnly}`);
        const data = await response.json();
        
        if (data.success && data.topics.length > 0) {
            currentTopics = data.topics;
            renderTopics(data.topics);
        } else {
            const message = favoritesOnly 
                ? 'No favorited topics found. Star some topics to see them here!' 
                : 'No topics found. Try adjusting filters or start a new research session.';
            container.innerHTML = `<div class="empty-state"><p>${message}</p></div>`;
        }
    } catch (error) {
        console.error('Failed to load topics:', error);
        container.innerHTML = '<div class="empty-state"><p>❌ Failed to load topics. Please try again.</p></div>';
    }
}

// Render Topics
function renderTopics(topics) {
    const container = document.getElementById('results-container');
    
    const html = `
        <div class="topics-grid">
            ${topics.map(topic => renderTopicCard(topic)).join('')}
        </div>
    `;
    
    container.innerHTML = html;
    
    // Add click handlers for cards
    topics.forEach((topic, index) => {
        const card = document.getElementById(`topic-${index}`);
        card.addEventListener('click', (e) => {
            // Don't open modal if clicking the star button
            if (!e.target.closest('.favorite-btn')) {
                showTopicDetail(topic);
            }
        });
    });
    
    // Add click handlers for favorite buttons
    topics.forEach((topic, index) => {
        const btn = document.getElementById(`favorite-btn-${index}`);
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleFavorite(topic, index);
        });
    });
}

// Render Topic Card
function renderTopicCard(topic, index) {
    const score = topic.total_score || 0;
    const scoreClass = score >= 80 ? 'high-score' : score >= 60 ? 'medium-score' : '';
    const scoreTag = score >= 80 ? 'high' : score >= 60 ? 'medium' : '';
    const isFavorited = topic.favorited || false;
    const topicIndex = currentTopics.indexOf(topic);
    
    return `
        <div class="topic-card ${scoreClass}" id="topic-${topicIndex}">
            <div class="topic-header">
                <div class="topic-title">${escapeHtml(topic.title)}</div>
                <div class="topic-header-actions">
                    <button class="favorite-btn ${isFavorited ? 'favorited' : ''}" 
                            id="favorite-btn-${topicIndex}"
                            title="${isFavorited ? 'Remove from favorites' : 'Add to favorites'}">
                        ${isFavorited ? '⭐' : '☆'}
                    </button>
                    <div class="topic-score ${scoreTag}">${score.toFixed(0)}</div>
                </div>
            </div>
            <div class="topic-meta">
                <span>📂 ${topic.category || 'General'}</span>
                <span>📊 ${topic.competition_level || 'N/A'} Competition</span>
                ${topic.views_potential ? `<span>👁️ ${formatNumber(topic.views_potential)} views potential</span>` : ''}
            </div>
            <div class="topic-scores">
                <div class="score-item">
                    <div class="score-label">Importance</div>
                    <div class="score-value">${(topic.importance_score || 0).toFixed(0)}</div>
                </div>
                <div class="score-item">
                    <div class="score-label">Watchability</div>
                    <div class="score-value">${(topic.watchability_score || 0).toFixed(0)}</div>
                </div>
                <div class="score-item">
                    <div class="score-label">Monetization</div>
                    <div class="score-value">${(topic.monetization_score || 0).toFixed(0)}</div>
                </div>
                <div class="score-item">
                    <div class="score-label">Popularity</div>
                    <div class="score-value">${(topic.popularity_score || 0).toFixed(0)}</div>
                </div>
                <div class="score-item">
                    <div class="score-label">Innovation</div>
                    <div class="score-value">${(topic.innovation_score || 0).toFixed(0)}</div>
                </div>
            </div>
        </div>
    `;
}

// Show Topic Detail
function showTopicDetail(topic) {
    const modal = document.getElementById('topic-modal');
    const detailContainer = document.getElementById('topic-detail');
    
    const html = `
        <h2>${escapeHtml(topic.title)}</h2>
        <p><strong>Total Score:</strong> ${(topic.total_score || 0).toFixed(0)}/100</p>
        <p><strong>Category:</strong> ${topic.category || 'General'}</p>
        <p><strong>Competition:</strong> ${topic.competition_level || 'N/A'}</p>
        
        <h3 style="margin-top: 20px;">Detailed Scores</h3>
        <div class="topic-scores" style="margin-bottom: 20px;">
            <div class="score-item">
                <div class="score-label">Importance</div>
                <div class="score-value">${(topic.importance_score || 0).toFixed(0)}</div>
            </div>
            <div class="score-item">
                <div class="score-label">Watchability</div>
                <div class="score-value">${(topic.watchability_score || 0).toFixed(0)}</div>
            </div>
            <div class="score-item">
                <div class="score-label">Monetization</div>
                <div class="score-value">${(topic.monetization_score || 0).toFixed(0)}</div>
            </div>
            <div class="score-item">
                <div class="score-label">Popularity</div>
                <div class="score-value">${(topic.popularity_score || 0).toFixed(0)}</div>
            </div>
            <div class="score-item">
                <div class="score-label">Innovation</div>
                <div class="score-value">${(topic.innovation_score || 0).toFixed(0)}</div>
            </div>
        </div>
        
        ${topic.recommended_angle ? `
            <h3>Recommended Angle</h3>
            <p>${escapeHtml(topic.recommended_angle)}</p>
        ` : ''}
        
        ${topic.keywords && topic.keywords.length > 0 ? `
            <h3>Keywords</h3>
            <p>${topic.keywords.map(k => `<span style="background: #e5e7eb; padding: 4px 8px; border-radius: 4px; margin-right: 5px;">${escapeHtml(k)}</span>`).join('')}</p>
        ` : ''}
        
        ${topic.notes ? `
            <h3>Notes</h3>
            <p>${escapeHtml(topic.notes)}</p>
        ` : ''}
        
        ${topic.ai_analysis ? `
            <details style="margin-top: 20px;">
                <summary style="cursor: pointer; font-weight: 600;">AI Analysis (Full)</summary>
                <pre style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin-top: 10px; overflow-x: auto; white-space: pre-wrap;">${escapeHtml(topic.ai_analysis)}</pre>
            </details>
        ` : ''}
        
        <p style="margin-top: 20px; color: #6b7280; font-size: 0.9rem;">
            <strong>Researched:</strong> ${new Date(topic.timestamp).toLocaleString()}
        </p>
    `;
    
    detailContainer.innerHTML = html;
    modal.classList.add('show');
}

// Toggle Favorite
async function toggleFavorite(topic, index) {
    const btn = document.getElementById(`favorite-btn-${index}`);
    const originalIcon = btn.textContent;
    
    // Show loading state
    btn.disabled = true;
    btn.textContent = '⏳';
    
    try {
        // Get the document ID from the topic
        const topicId = topic._id || topic.doc_id;
        if (!topicId) {
            throw new Error('Topic ID not found');
        }
        
        const response = await fetch(`${API_BASE}/api/topics/${topicId}/favorite`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update the topic in currentTopics
            topic.favorited = data.favorited;
            
            // Update button
            btn.classList.toggle('favorited', data.favorited);
            btn.textContent = data.favorited ? '⭐' : '☆';
            btn.title = data.favorited ? 'Remove from favorites' : 'Add to favorites';
            
            // If we're in favorites-only mode and just unfavorited, reload
            const favoritesOnly = document.getElementById('favorites-only').checked;
            if (favoritesOnly && !data.favorited) {
                await loadTopics();
            }
        } else {
            throw new Error(data.error || 'Failed to toggle favorite');
        }
    } catch (error) {
        console.error('Failed to toggle favorite:', error);
        btn.textContent = originalIcon;
        alert(`Failed to update favorite: ${error.message}`);
    } finally {
        btn.disabled = false;
    }
}

// Close Modal
function closeModal() {
    document.getElementById('topic-modal').classList.remove('show');
}

// Load Analytics
async function loadAnalytics() {
    try {
        const response = await fetch(`${API_BASE}/api/analytics?days=7`);
        const data = await response.json();
        
        if (data.success) {
            const analytics = data.analytics;
            
            document.getElementById('total-sessions').textContent = analytics.total_sessions || 0;
            document.getElementById('topics-researched').textContent = analytics.topics_researched || 0;
            document.getElementById('high-quality-topics').textContent = analytics.high_quality_topics || 0;
            document.getElementById('avg-score').textContent = (analytics.avg_score || 0).toFixed(1);
        }
    } catch (error) {
        console.error('Failed to load analytics:', error);
    }
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

