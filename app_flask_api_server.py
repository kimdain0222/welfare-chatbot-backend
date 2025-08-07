from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app, origins=['https://welfarechatbot02.netlify.app', 'http://localhost:3000'])  # React에서 API 호출할 수 있도록 CORS 설정

# DB 파일 경로
DB_PATH = "welfare_policies.db"

def get_db_connection():
    """데이터베이스 연결"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
    return conn

@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return jsonify({"status": "healthy", "message": "API 서버가 정상 작동 중입니다!"})

@app.route('/api/policies/region/<region>', methods=['GET'])
def get_policies_by_region(region):
    """지역별 정책 조회"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, url, region, age_range, application_period, conditions, benefits
            FROM welfare_policies
            WHERE region = ?
            ORDER BY title
        ''', (region,))
        
        policies = []
        for row in cursor.fetchall():
            policy = dict(row)
            if policy['age_range']:
                policy['age_range'] = json.loads(policy['age_range'])
            else:
                policy['age_range'] = []
            policies.append(policy)
        
        conn.close()
        return jsonify({
            "success": True,
            "region": region,
            "count": len(policies),
            "policies": policies
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/policies', methods=['GET'])
def get_all_policies():
    """모든 정책 조회"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, url, region, age_range, application_period, conditions, benefits
            FROM welfare_policies
            ORDER BY region, title
        ''')
        
        policies = []
        for row in cursor.fetchall():
            policy = dict(row)
            if policy['age_range']:
                policy['age_range'] = json.loads(policy['age_range'])
            else:
                policy['age_range'] = []
            policies.append(policy)
        
        conn.close()
        return jsonify({
            "success": True,
            "count": len(policies),
            "policies": policies
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 복지정책 API 서버 시작...")
    print("📊 사용 가능한 엔드포인트:")
    print("   GET /api/health - 서버 상태 확인")
    print("   GET /api/policies - 모든 정책 조회")
    print("   GET /api/policies/region/<region> - 지역별 정책 조회")
    print("\n🌐 서버 주소: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 