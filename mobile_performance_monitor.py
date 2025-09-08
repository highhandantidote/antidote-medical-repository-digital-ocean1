"""
Mobile Performance Monitoring System
Tracks Core Web Vitals and mobile performance metrics
"""

from flask import Blueprint, jsonify, request
import time
import logging

logger = logging.getLogger(__name__)

mobile_monitor_bp = Blueprint('mobile_monitor', __name__)

class MobilePerformanceMonitor:
    """Monitor mobile performance and Core Web Vitals"""
    
    def __init__(self):
        self.performance_data = []
        self.mobile_thresholds = {
            'lcp': 2.5,  # Largest Contentful Paint (seconds)
            'fid': 0.1,  # First Input Delay (seconds) 
            'cls': 0.1   # Cumulative Layout Shift
        }
    
    def track_page_load(self, load_time, device_type, page_url):
        """Track page load performance"""
        performance_entry = {
            'timestamp': time.time(),
            'load_time': load_time,
            'device_type': device_type,
            'page_url': page_url,
            'is_good_performance': load_time < 1.0  # Under 1 second
        }
        
        self.performance_data.append(performance_entry)
        
        # Keep only last 1000 entries
        if len(self.performance_data) > 1000:
            self.performance_data = self.performance_data[-1000:]
            
        # Log slow mobile pages
        if device_type == 'mobile' and load_time > 2.0:
            logger.warning(f"Slow mobile page load: {page_url} took {load_time:.2f}s")
    
    def get_mobile_performance_stats(self):
        """Get mobile performance statistics"""
        mobile_data = [d for d in self.performance_data if d['device_type'] == 'mobile']
        
        if not mobile_data:
            return {'status': 'no_data'}
        
        avg_load_time = sum(d['load_time'] for d in mobile_data) / len(mobile_data)
        good_performance_rate = sum(1 for d in mobile_data if d['is_good_performance']) / len(mobile_data)
        
        return {
            'total_mobile_requests': len(mobile_data),
            'average_load_time': round(avg_load_time, 2),
            'good_performance_rate': round(good_performance_rate * 100, 1),
            'mobile_health': 'good' if good_performance_rate > 0.75 else 'needs_improvement'
        }

# Global monitor instance
mobile_monitor = MobilePerformanceMonitor()

@mobile_monitor_bp.route('/api/mobile/performance-stats')
def get_mobile_stats():
    """Get mobile performance statistics"""
    stats = mobile_monitor.get_mobile_performance_stats()
    return jsonify(stats)

@mobile_monitor_bp.route('/api/mobile/track-performance', methods=['POST'])
def track_mobile_performance():
    """Track mobile performance metrics"""
    try:
        data = request.get_json()
        load_time = data.get('load_time', 0)
        device_type = data.get('device_type', 'unknown')
        page_url = data.get('page_url', '/')
        
        mobile_monitor.track_page_load(load_time, device_type, page_url)
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error tracking mobile performance: {e}")
        return jsonify({'success': False, 'error': str(e)})

def initialize_mobile_monitoring(app):
    """Initialize mobile performance monitoring"""
    app.register_blueprint(mobile_monitor_bp)
    logger.info("✅ Mobile performance monitoring initialized")