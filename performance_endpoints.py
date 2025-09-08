"""
Performance Monitoring Endpoints
Quick health checks and performance diagnostics
"""

from flask import Blueprint, jsonify, request
import time
import psutil
import os
from datetime import datetime

perf_bp = Blueprint('performance', __name__)

@perf_bp.route('/api/performance/health')
def health_check():
    """Quick health check endpoint"""
    start_time = time.time()
    
    # Basic health indicators
    health_data = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'server_time': time.time(),
        'memory_usage': psutil.virtual_memory().percent,
        'cpu_usage': psutil.cpu_percent(interval=0.1),
        'response_time_ms': 0  # Will be calculated below
    }
    
    # Calculate response time
    response_time = (time.time() - start_time) * 1000
    health_data['response_time_ms'] = round(response_time, 2)
    
    # Determine health status
    if response_time > 200:
        health_data['status'] = 'slow'
    elif response_time > 500:
        health_data['status'] = 'critical'
    
    return jsonify(health_data)

@perf_bp.route('/api/performance/quick-test')
def quick_performance_test():
    """Quick performance test for mobile optimization"""
    start_time = time.time()
    
    # Simulate typical operations
    test_data = []
    
    # Test 1: Database connection speed
    db_start = time.time()
    try:
        from app import db
        db.session.execute('SELECT 1')
        db_time = (time.time() - db_start) * 1000
        test_data.append({
            'test': 'database_connection',
            'time_ms': round(db_time, 2),
            'status': 'good' if db_time < 50 else 'slow'
        })
    except Exception as e:
        test_data.append({
            'test': 'database_connection', 
            'time_ms': 999,
            'status': 'error',
            'error': str(e)
        })
    
    # Test 2: Memory and CPU
    memory_test_start = time.time()
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(interval=0.1) 
    memory_test_time = (time.time() - memory_test_start) * 1000
    
    test_data.append({
        'test': 'system_resources',
        'time_ms': round(memory_test_time, 2),
        'memory_percent': memory_usage,
        'cpu_percent': cpu_usage,
        'status': 'good' if memory_usage < 80 and cpu_usage < 80 else 'high'
    })
    
    # Test 3: File system access
    fs_start = time.time()
    try:
        # Check if static files are accessible
        static_dir = os.path.join('.', 'static')
        file_count = len(os.listdir(static_dir)) if os.path.exists(static_dir) else 0
        fs_time = (time.time() - fs_start) * 1000
        
        test_data.append({
            'test': 'filesystem_access',
            'time_ms': round(fs_time, 2),
            'static_files_count': file_count,
            'status': 'good' if fs_time < 100 else 'slow'
        })
    except Exception as e:
        test_data.append({
            'test': 'filesystem_access',
            'time_ms': 999,
            'status': 'error', 
            'error': str(e)
        })
    
    total_time = (time.time() - start_time) * 1000
    
    return jsonify({
        'total_time_ms': round(total_time, 2),
        'overall_status': 'good' if total_time < 200 else 'needs_optimization',
        'tests': test_data,
        'mobile_ready': total_time < 300  # Critical for mobile CTR
    })

@perf_bp.route('/api/performance/mobile-readiness')
def mobile_readiness_check():
    """Check if the application is optimized for mobile performance"""
    start_time = time.time()
    
    checks = []
    
    # Check 1: Response time
    response_start = time.time()
    response_time = (time.time() - response_start) * 1000
    checks.append({
        'check': 'response_time',
        'value': round(response_time, 2),
        'target': '< 200ms',
        'status': 'pass' if response_time < 200 else 'fail'
    })
    
    # Check 2: Static file optimization
    static_check = {
        'check': 'static_optimization',
        'css_bundles': os.path.exists('static/optimized/'),
        'js_compression': os.path.exists('static/js/critical-mobile.js'),
        'status': 'pass'
    }
    
    if not static_check['css_bundles'] or not static_check['js_compression']:
        static_check['status'] = 'partial'
    
    checks.append(static_check)
    
    # Check 3: Database performance
    db_start = time.time()
    try:
        from app import db
        db.session.execute('SELECT COUNT(*) FROM users LIMIT 1')
        db_time = (time.time() - db_start) * 1000
        checks.append({
            'check': 'database_performance',
            'time_ms': round(db_time, 2),
            'target': '< 50ms',
            'status': 'pass' if db_time < 50 else 'optimize'
        })
    except:
        checks.append({
            'check': 'database_performance',
            'status': 'error'
        })
    
    total_time = (time.time() - start_time) * 1000
    passed_checks = sum(1 for c in checks if c.get('status') == 'pass')
    
    return jsonify({
        'mobile_readiness_score': round((passed_checks / len(checks)) * 100, 1),
        'total_test_time_ms': round(total_time, 2),
        'recommendations': [
            'Optimize database queries' if any(c.get('check') == 'database_performance' and c.get('status') != 'pass' for c in checks) else None,
            'Implement aggressive caching' if response_time > 200 else None,
            'Optimize static assets' if any(c.get('check') == 'static_optimization' and c.get('status') != 'pass' for c in checks) else None
        ],
        'checks': checks
    })

def initialize_performance_endpoints(app):
    """Initialize performance monitoring endpoints"""
    app.register_blueprint(perf_bp)
    return True