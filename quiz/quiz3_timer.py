from flask import Flask, request, jsonify
from datetime import datetime
import re

app = Flask(__name__)

next_session_id = 1
sessions = []

def name_valid(task_name):
    if not task_name:
        return False, {
        "error": "Lack task name",
        "message": "Task name is required"
        }
    
    if len(task_name) < 3 or len(task_name)> 20:
        return False, {
        "error": "Invalid task name",
        "message": "Task name must be between 3 and 20 characters"
        }
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', task_name):
        return False, "Task name must contain only alphanumeric characters, hyphens, and underscores"
    
    
    return True, None

# JSON does NOT support Python datetime objects
# need to convert it to isoformat
def print_session(session):
    result = {
        'session_id': session['session_id'],
        'task_name': session['task_name'],
        #'started_at': session['started_at'].isoformat(),   # "2024-01-15T14:30:00"
        'started_at': str(session['started_at']),           # "2024-01-15 14:30:00"
        'status': session['status']
    }

    if 'stopped_at' in session and session['stopped_at']:
        # result['stopped_at'] = session['stopped_at'].isoformat()
        result['stopped_at'] = str(session['stopped_at'])
    else:
        result['stopped_at'] = None

    if session['status'] == 'completed':
        result['duration_seconds'] = session['duration_seconds']
    else:
    # For running sessions, calculate from start to now
        result['duration_seconds'] = int((datetime.now() - session['started_at']).total_seconds())

    return result

@app.route('/sessions/start', methods=['POST'])
def start_timer():
    # check task_name
    data = request.get_json()
    if not data:
        return {"error": "Lack task name"}, 400
    
    task_name = data.get('task_name')

    is_valid, error_content = name_valid(task_name)
    if not is_valid:
        return error_content
    
    # create a new session
    global next_session_id

    new_session = {
        "session_id": next_session_id,
        "task_name": task_name,
        "started_at": datetime.now(),
        "status": "running"
    }
    sessions.append(new_session)
    next_session_id += 1

    return print_session(new_session), 201

@app.route('/sessions/<int:id>/stop', methods=['POST'])
def stop_session(id):
    # check such id in sessions
    for session in sessions:
        if session.get('session_id') == id:
            if session.get('status') != "running":
                return {
                    "error": "Session already stopped",
                    "message": f"Session {id} was already stopped"
                    }, 400
            else:
                session['stopped_at'] = datetime.now()
                session['duration_seconds'] = int((session['stopped_at'] - session['started_at']).total_seconds())
                session['status'] = "completed"
                return print_session(session), 200
        
    return {
        "error": "Session not found",
        "message": f"No session with ID {id}"
        }, 404

@app.route('/sessions', methods=['GET'])
def get_sessions():
    filter_status = request.args.get("status")
    
    if not filter_status:
        filtered_sessions = sessions
    else:
        if filter_status not in ['running', 'completed']:
            return {"error": "wrong status"}
        else:
            filtered_sessions = [s for s in sessions if s.get('status')==filter_status]
    

    return {"sessions": [print_session(s) for s in filtered_sessions],
            "total": len(filtered_sessions)
            }, 200
    

    
    
    
@app.route('/sessions/<int:id>', methods=['GET'])
def get_session(id):  
    # check such id in sessions
    for session in sessions:
        if session.get('session_id') == id:
            return print_session(session), 200
    
    return {
        "error": "Session not found",
        "message": f"No session with ID {id}"
    }, 404

@app.route('/sessions/<int:id>', methods=['DELETE'])
def delete_session(id):  
    # check such id in sessions
    for session in sessions:
        if session.get('session_id') == id:
            sessions.remove(session)
            return {
                "message": "session deleted:", 
                "session": print_session(session)
            }, 200
    
    return {
        "error": "Session not found",
        "message": f"No session with ID {id}"
    }

if __name__ == '__main__':
    app.run(debug=True)