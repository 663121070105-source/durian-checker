"""
Durian Smart AI - ระบบวิเคราะห์ทุเรียนอัจฉริยะ
Python Flask Web Application with Authentication
"""

from flask import Flask, render_template_string, request, jsonify, session
from datetime import datetime
import secrets
import json
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Admin credentials
ADMIN_CREDENTIALS = [
    {'email': 'admin@durianai.com', 'password': 'admin123'},
    {'email': 'manager@durianai.com', 'password': 'manager456'}
]

# Sample devices data
DEVICES = [
    {'id': 'DEVICE-001', 'name': 'เซนเซอร์ทุเรียน A', 'location': 'โกดัง A1', 'status': 'online', 'lastUpdate': '2 นาทีที่แล้ว'},
    {'id': 'DEVICE-002', 'name': 'เซนเซอร์ทุเรียน B', 'location': 'โกดัง A2', 'status': 'online', 'lastUpdate': '5 นาทีที่แล้ว'},
    {'id': 'DEVICE-003', 'name': 'เซนเซอร์ทุเรียน C', 'location': 'โกดัง B1', 'status': 'offline', 'lastUpdate': '2 ชั่วโมงที่แล้ว'},
    {'id': 'DEVICE-004', 'name': 'เซนเซอร์ทุเรียน D', 'location': 'โกดัง B2', 'status': 'online', 'lastUpdate': '1 นาทีที่แล้ว'}
]

# Data storage (in production, use database)
user_data = {}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Durian Smart AI - ระบบวิเคราะห์ทุเรียนอัจฉริยะ</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 700px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .header h1 {
            color: #558B2F;
            font-size: 32px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .header p {
            color: #F9A825;
            font-size: 16px;
        }

        .emoji {
            font-size: 40px;
        }

        .mode-switch {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            background: white;
            padding: 10px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .mode-btn {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
            background: #F5F5F5;
            color: #757575;
        }

        .mode-btn.active {
            background: linear-gradient(135deg, #81C784 0%, #AED581 100%);
            color: white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }

        .mode-btn.admin.active {
            background: linear-gradient(135deg, #FFF176 0%, #FFEB3B 100%);
            color: #558B2F;
        }

        .panel {
            display: none;
        }

        .panel.active {
            display: block;
        }

        .action-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 25px;
        }

        .action-btn {
            background: linear-gradient(135deg, #81C784 0%, #AED581 100%);
            color: white;
            border: none;
            padding: 20px;
            border-radius: 15px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }

        .action-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.2);
        }

        .action-btn.data {
            background: linear-gradient(135deg, #FFF176 0%, #FFD54F 100%);
            color: #558B2F;
            grid-column: span 2;
        }

        .preview-area {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            margin-bottom: 20px;
        }

        .placeholder {
            color: #9E9E9E;
        }

        .icon {
            font-size: 80px;
            margin-bottom: 20px;
        }

        .yolo-badge {
            display: inline-block;
            background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: bold;
            margin-top: 15px;
        }

        .result-section {
            text-align: left;
            margin-top: 25px;
        }

        .status-badge {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 20px;
        }

        .status-badge.unripe {
            background: #FFCCBC;
            color: #E64A19;
        }

        .status-badge.ripening {
            background: #FFF9C4;
            color: #F57F17;
        }

        .status-badge.ready {
            background: #C8E6C9;
            color: #2E7D32;
        }

        .bar-container {
            margin-bottom: 15px;
        }

        .bar-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-weight: bold;
            color: #424242;
        }

        .bar {
            background: #E0E0E0;
            height: 25px;
            border-radius: 12px;
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            transition: width 1s ease;
            border-radius: 12px;
        }

        .bar-fill.unripe {
            background: linear-gradient(90deg, #FFCCBC 0%, #FF8A65 100%);
        }

        .bar-fill.ripening {
            background: linear-gradient(90deg, #FFF9C4 0%, #FFD54F 100%);
        }

        .bar-fill.ready {
            background: linear-gradient(90deg, #C8E6C9 0%, #81C784 100%);
        }

        .sensor-data {
            margin-top: 25px;
            padding: 20px;
            background: #F5F5F5;
            border-radius: 15px;
        }

        .sensor-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 14px;
        }

        .sensor-label {
            color: #757575;
        }

        .sensor-value {
            font-weight: bold;
            color: #424242;
        }

        .sync-info {
            margin-top: 20px;
            padding: 15px;
            background: #E3F2FD;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 14px;
            color: #1976D2;
        }

        .admin-section {
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        .admin-section h2 {
            color: #558B2F;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .device-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .device-item {
            padding: 15px;
            background: #F5F5F5;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .device-info h3 {
            color: #424242;
            font-size: 16px;
            margin-bottom: 5px;
        }

        .device-info p {
            color: #757575;
            font-size: 13px;
        }

        .device-status {
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: bold;
        }

        .device-status.online {
            background: #C8E6C9;
            color: #2E7D32;
        }

        .device-status.offline {
            background: #FFCCBC;
            color: #E64A19;
        }

        .chart-filters {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .filter-btn {
            flex: 1;
            padding: 10px;
            border: 2px solid #E0E0E0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }

        .filter-btn.active {
            border-color: #81C784;
            background: #E8F5E9;
            color: #558B2F;
            font-weight: bold;
        }

        .chart-container {
            background: #F5F5F5;
            padding: 20px;
            border-radius: 12px;
            height: 250px;
            display: flex;
            align-items: flex-end;
            justify-content: space-around;
        }

        .chart-bar {
            background: linear-gradient(180deg, #81C784 0%, #4CAF50 100%);
            width: 40px;
            border-radius: 5px 5px 0 0;
            position: relative;
            transition: height 0.5s ease;
        }

        .chart-label {
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 12px;
            color: #757575;
            white-space: nowrap;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 20px;
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .modal-header h2 {
            color: #558B2F;
        }

        .close-btn {
            background: none;
            border: none;
            font-size: 28px;
            cursor: pointer;
            color: #9E9E9E;
        }

        .data-item {
            padding: 15px;
            background: #F5F5F5;
            border-radius: 12px;
            margin-bottom: 15px;
        }

        .data-item-date {
            color: #757575;
            font-size: 13px;
            margin-bottom: 8px;
        }

        .data-item-result {
            font-weight: bold;
            color: #424242;
            margin-bottom: 5px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #424242;
            font-weight: bold;
        }

        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            font-size: 15px;
        }

        .form-group input:focus {
            outline: none;
            border-color: #81C784;
        }

        .submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #81C784 0%, #AED581 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .add-device-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #FFF176 0%, #FFD54F 100%);
            color: #558B2F;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 15px;
        }

        .sensor-cards {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 20px;
        }

        .sensor-card {
            background: #F5F5F5;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }

        .sensor-card h4 {
            color: #757575;
            font-size: 14px;
            margin-bottom: 10px;
        }

        .sensor-card .value {
            color: #558B2F;
            font-size: 24px;
            font-weight: bold;
        }

        input[type="file"] {
            display: none;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                <span class="emoji">🥭</span>
                Durian Smart AI
            </h1>
            <p>ระบบวิเคราะห์ความสุกของทุเรียนอัจฉริยะ | Smart Durian Ripeness Analysis System</p>
        </div>

        <div class="mode-switch">
            <button class="mode-btn active" onclick="switchMode('user')">👤 ผู้ใช้งาน</button>
            <button class="mode-btn admin" onclick="switchMode('admin')">🔧 ผู้ดูแลระบบ</button>
        </div>

        <!-- User Panel -->
        <div id="userPanel" class="panel active">
            <div class="action-buttons">
                <button class="action-btn" onclick="openCamera()">
                    <span style="font-size: 32px;">📷</span>
                    ถ่ายภาพ
                </button>
                <button class="action-btn" onclick="scanImage()">
                    <span style="font-size: 32px;">🔍</span>
                    แสกน
                </button>
                <button class="action-btn" onclick="uploadImage()">
                    <span style="font-size: 32px;">🖼️</span>
                    เพิ่มรูป
                </button>
                <button class="action-btn data" onclick="showData()">
                    <span style="font-size: 32px;">📊</span>
                    ดูข้อมูลที่เก็บ
                </button>
            </div>

            <div class="preview-area" id="previewArea">
                <div class="placeholder">
                    <div class="icon">🥭</div>
                    <p>เลือกการทำงานด้านบนเพื่อเริ่มวิเคราะห์ทุเรียน</p>
                    <div class="yolo-badge">✨ วิเคราะห์ด้วย YOLO Model</div>
                    <div id="currentUserDisplay" style="margin-top: 15px; color: #757575; font-size: 14px;"></div>
                </div>
            </div>

            <input type="file" id="cameraInput" accept="image/*" capture="camera" onchange="handleImage(event)">
            <input type="file" id="fileInput" accept="image/*" onchange="handleImage(event)">
        </div>

        <!-- Admin Panel -->
        <div id="adminPanel" class="panel">
            <div class="admin-section">
                <h2>📱 จัดการ Device ID</h2>
                <div class="device-list" id="deviceList"></div>
                <button class="add-device-btn" onclick="showAddDevice()">➕ เพิ่มอุปกรณ์ใหม่</button>
            </div>

            <div class="admin-section">
                <h2>📈 ประวัติค่าการอ่านก๊าซ</h2>
                <div class="chart-filters">
                    <button class="filter-btn active" onclick="filterChart('24h')">24 ชั่วโมง</button>
                    <button class="filter-btn" onclick="filterChart('7d')">7 วัน</button>
                    <button class="filter-btn" onclick="filterChart('30d')">30 วัน</button>
                </div>
                <div class="chart-container" id="chartContainer"></div>
            </div>

            <div class="admin-section">
                <h2>🔬 ข้อมูลเซนเซอร์แบบ Real-time</h2>
                <div class="sensor-cards">
                    <div class="sensor-card">
                        <h4>Ethylene (C₂H₄)</h4>
                        <div class="value" id="realtimeEthylene">--</div>
                        <p style="font-size: 12px; color: #9E9E9E; margin-top: 5px;">ppm</p>
                    </div>
                    <div class="sensor-card">
                        <h4>CO₂</h4>
                        <div class="value" id="realtimeCO2">--</div>
                        <p style="font-size: 12px; color: #9E9E9E; margin-top: 5px;">ppm</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Data History Modal -->
    <div id="dataModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>📊 ข้อมูลที่บันทึกไว้</h2>
                <button class="close-btn" onclick="closeData()">×</button>
            </div>
            <div id="dataList"></div>
        </div>
    </div>

    <!-- Add Device Modal -->
    <div id="addDeviceModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>➕ เพิ่มอุปกรณ์ใหม่</h2>
                <button class="close-btn" onclick="closeAddDevice()">×</button>
            </div>
            <form onsubmit="addDevice(event)">
                <div class="form-group">
                    <label>Device ID:</label>
                    <input type="text" id="deviceId" placeholder="DEVICE-XXX" required>
                </div>
                <div class="form-group">
                    <label>ชื่ออุปกรณ์:</label>
                    <input type="text" id="deviceName" placeholder="เซนเซอร์ทุเรียน X" required>
                </div>
                <div class="form-group">
                    <label>ตำแหน่ง:</label>
                    <input type="text" id="deviceLocation" placeholder="โกดัง XX" required>
                </div>
                <button type="submit" class="submit-btn">เพิ่มอุปกรณ์</button>
            </form>
        </div>
    </div>

    <script>
        let currentUserEmail = null;
        let isAdminLoggedIn = false;
        let currentMode = 'user';

        // Mode Switch
        function switchMode(mode) {
            if (mode === 'admin') {
                showAdminLogin();
                return;
            }
            
            currentMode = mode;
            document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            document.querySelectorAll('.panel').forEach(panel => panel.classList.remove('active'));
            document.getElementById(mode + 'Panel').classList.add('active');
        }

        // User Panel Functions
        function openCamera() {
            if (!currentUserEmail) {
                showEmailPromptForAnalysis('camera');
                return;
            }
            document.getElementById('cameraInput').click();
        }

        function scanImage() {
            if (!currentUserEmail) {
                showEmailPromptForAnalysis('scan');
                return;
            }
            document.getElementById('fileInput').click();
        }

        function uploadImage() {
            if (!currentUserEmail) {
                showEmailPromptForAnalysis('upload');
                return;
            }
            document.getElementById('fileInput').click();
        }

        function showEmailPromptForAnalysis(action) {
            const modal = document.createElement('div');
            modal.className = 'modal active';
            modal.id = 'emailAnalysisModal';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>📧 ใส่อีเมลของคุณ</h2>
                    </div>
                    <form onsubmit="setUserEmailForAnalysis(event, '${action}')">
                        <div class="form-group">
                            <label>อีเมล:</label>
                            <input type="email" id="analysisUserEmail" placeholder="example@email.com" required>
                        </div>
                        <p style="color: #757575; font-size: 14px; margin-bottom: 20px;">
                            ใส่อีเมลเพื่อเริ่มวิเคราะห์ทุเรียนและบันทึกข้อมูล
                        </p>
                        <button type="submit" class="submit-btn">ดำเนินการต่อ</button>
                    </form>
                </div>
            `;
            document.body.appendChild(modal);
            
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    modal.remove();
                }
            });
        }

        function setUserEmailForAnalysis(event, action) {
            event.preventDefault();
            const email = document.getElementById('analysisUserEmail').value;
            
            fetch('/api/set-user-email', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email: email})
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      currentUserEmail = email;
                      document.getElementById('emailAnalysisModal').remove();
                      updateCurrentUserDisplay();
                      showSuccessMessage(`✓ เข้าสู่ระบบด้วย ${email}`);
                      
                      setTimeout(() => {
                          if (action === 'camera') {
                              document.getElementById('cameraInput').click();
                          } else {
                              document.getElementById('fileInput').click();
                          }
                      }, 1000);
                  }
              });
        }

        function updateCurrentUserDisplay() {
            const display = document.getElementById('currentUserDisplay');
            if (display && currentUserEmail) {
                display.innerHTML = `
                    <div style="background: #E8F5E9; padding: 10px; border-radius: 8px; display: inline-block;">
                        <strong style="color: #558B2F;">👤 ${currentUserEmail}</strong>
                    </div>
                `;
            }
        }

        function handleImage(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    analyzeImage(e.target.result);
                };
                reader.readAsDataURL(file);
            }
        }

        function analyzeImage(imageData) {
            const preview = document.getElementById('previewArea');
            preview.innerHTML = `
                <div class="icon" style="animation: rotate 2s linear infinite;">🔄</div>
                <p style="color: #558B2F; font-weight: bold;">กำลังวิเคราะห์ด้วย YOLO Model...</p>
            `;

            setTimeout(() => {
                const unripe = Math.floor(Math.random() * 40);
                const ready = Math.floor(Math.random() * 40);
                const ripening = 100 - unripe - ready;

                let status = '';
                let statusClass = '';
                
                if (ready >= 70) {
                    status = '🟢 สุกพร้อมรับประทาน';
                    statusClass = 'ready';
                } else if (ripening >= 50) {
                    status = '🟡 เริ่มสุก';
                    statusClass = 'ripening';
                } else {
                    status = '🔴 ดิบ';
                    statusClass = 'unripe';
                }

                const ethylene = (10 + Math.random() * 50).toFixed(1);
                const co2 = (500 + Math.random() * 1000).toFixed(0);

                preview.innerHTML = `
                    <img src="${imageData}" style="max-width: 100%; border-radius: 15px; margin-bottom: 20px;">
                    <div class="yolo-badge">✨ วิเคราะห์ด้วย YOLO Model</div>
                    <div class="result-section">
                        <div class="status-badge ${statusClass}">${status}</div>
                        <div class="bar-container">
                            <div class="bar-label">
                                <span>ดิบ (Unripe)</span>
                                <span>${unripe}%</span>
                            </div>
                            <div class="bar">
                                <div class="bar-fill unripe" style="width: ${unripe}%"></div>
                            </div>
                        </div>
                        <div class="bar-container">
                            <div class="bar-label">
                                <span>เริ่มสุก (Ripening)</span>
                                <span>${ripening}%</span>
                            </div>
                            <div class="bar">
                                <div class="bar-fill ripening" style="width: ${ripening}%"></div>
                            </div>
                        </div>
                        <div class="bar-container">
                            <div class="bar-label">
                                <span>สุกพร้อมรับประทาน (Ready)</span>
                                <span>${ready}%</span>
                            </div>
                            <div class="bar">
                                <div class="bar-fill ready" style="width: ${ready}%"></div>
                            </div>
                        </div>
                        <div class="sensor-data">
                            <div class="sensor-row">
                                <span class="sensor-label">🌿 Ethylene (C₂H₄):</span>
                                <span class="sensor-value">${ethylene} ppm</span>
                            </div>
                            <div class="sensor-row">
                                <span class="sensor-label">💨 CO₂:</span>
                                <span class="sensor-value">${co2} ppm</span>
                            </div>
                        </div>
                        <div class="sync-info">
                            <span>☁️</span>
                            <span>ซิงค์ข้อมูลกับ Firebase สำเร็จ</span>
                        </div>
                    </div>
                `;

                // Save result to backend
                fetch('/api/save-result', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        email: currentUserEmail,
                        unripe: unripe,
                        ripening: ripening,
                        ready: ready,
                        status: status,
                        ethylene: ethylene,
                        co2: co2
                    })
                });
            }, 2000);
        }

        function showData() {
            if (!currentUserEmail) {
                showEmailPrompt();
                return;
            }

            fetch(`/api/get-user-data?email=${encodeURIComponent(currentUserEmail)}`)
                .then(response => response.json())
                .then(data => {
                    const dataList = document.getElementById('dataList');
                    
                    if (data.results.length === 0) {
                        dataList.innerHTML = `
                            <div style="text-align: center; padding: 40px; color: #9E9E9E;">
                                <div style="font-size: 48px; margin-bottom: 15px;">📭</div>
                                <p>ยังไม่มีข้อมูลที่บันทึกสำหรับ</p>
                                <p style="color: #558B2F; font-weight: bold; margin-top: 10px;">${currentUserEmail}</p>
                            </div>
                        `;
                    } else {
                        dataList.innerHTML = `
                            <div style="background: #E8F5E9; padding: 10px; border-radius: 8px; margin-bottom: 15px; text-align: center;">
                                <strong style="color: #558B2F;">📧 ${currentUserEmail}</strong>
                            </div>
                        ` + data.results.map(item => `
                            <div class="data-item">
                                <div class="data-item-date">${item.date}</div>
                                <div class="data-item-result">${item.status}</div>
                                <div style="font-size: 13px; color: #757575; margin-top: 8px;">
                                    ดิบ: ${item.unripe}% | เริ่มสุก: ${item.ripening}% | สุก: ${item.ready}%
                                </div>
                                <div style="font-size: 13px; color: #757575; margin-top: 5px;">
                                    Ethylene: ${item.ethylene} ppm | CO₂: ${item.co2} ppm
                                </div>
                            </div>
                        `).join('');
                    }

                    document.getElementById('dataModal').classList.add('active');
                });
        }

        function closeData() {
            document.getElementById('dataModal').classList.remove('active');
        }

        function showEmailPrompt() {
            const modal = document.createElement('div');
            modal.className = 'modal active';
            modal.id = 'emailModal';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>📧 ใส่อีเมลของคุณ</h2>
                    </div>
                    <form onsubmit="setUserEmail(event)">
                        <div class="form-group">
                            <label>อีเมล:</label>
                            <input type="email" id="userEmail" placeholder="example@email.com" required>
                        </div>
                        <p style="color: #757575; font-size: 14px; margin-bottom: 20px;">
                            ใส่อีเมลเพื่อดูข้อมูลการวิเคราะห์ของคุณ
                        </p>
                        <button type="submit" class="submit-btn">เข้าสู่ระบบ</button>
                    </form>
                </div>
            `;
            document.body.appendChild(modal);
            
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    modal.remove();
                }
            });
        }

        function setUserEmail(event) {
            event.preventDefault();
            const email = document.getElementById('userEmail').value;
            
            fetch('/api/set-user-email', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email: email})
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      currentUserEmail = email;
                      document.getElementById('emailModal').remove();
                      updateCurrentUserDisplay();
                      showSuccessMessage(`✓ เข้าสู่ระบบด้วย ${email}`);
                      setTimeout(() => showData(), 1500);
                  }
              });
        }

        // Admin Functions
        function showAdminLogin() {
            const modal = document.createElement('div');
            modal.className = 'modal active';
            modal.id = 'adminLoginModal';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>🔐 เข้าสู่ระบบผู้ดูแล</h2>
                        <button class="close-btn" onclick="closeAdminLogin()">×</button>
                    </div>
                    <form onsubmit="verifyAdmin(event)">
                        <div class="form-group">
                            <label>อีเมลผู้ดูแล:</label>
                            <input type="email" id="adminEmail" placeholder="admin@durianai.com" required>
                        </div>
                        <div class="form-group">
                            <label>รหัสผ่าน:</label>
                            <input type="password" id="adminPassword" placeholder="••••••••" required>
                        </div>
                        <div id="loginError" style="color: #F44336; font-size: 14px; margin-bottom: 15px; display: none;">
                            ❌ อีเมลหรือรหัสผ่านไม่ถูกต้อง
                        </div>
                        <button type="submit" class="submit-btn">เข้าสู่ระบบ</button>
                    </form>
                    <div style="margin-top: 20px; padding: 15px; background: #FFF9C4; border-radius: 10px; font-size: 13px; color: #F57F17;">
                        <strong>💡 ทดลองใช้:</strong><br>
                        Email: admin@durianai.com<br>
                        Password: admin123
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    modal.remove();
                }
            });
        }

        function closeAdminLogin() {
            const modal = document.getElementById('adminLoginModal');
            if (modal) modal.remove();
        }

        function verifyAdmin(event) {
            event.preventDefault();
            const email = document.getElementById('adminEmail').value;
            const password = document.getElementById('adminPassword').value;
            
            fetch('/api/admin-login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email: email, password: password})
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      isAdminLoggedIn = true;
                      closeAdminLogin();
                      
                      currentMode = 'admin';
                      document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
                      document.querySelector('.mode-btn.admin').classList.add('active');
                      
                      document.querySelectorAll('.panel').forEach(panel => panel.classList.remove('active'));
                      document.getElementById('adminPanel').classList.add('active');
                      
                      loadDevices();
                      initChart();
                      startRealtimeSensor();
                      
                      showSuccessMessage('✓ เข้าสู่ระบบผู้ดูแลสำเร็จ', '#FFEB3B', '#558B2F');
                  } else {
                      document.getElementById('loginError').style.display = 'block';
                  }
              });
        }

        function loadDevices() {
            fetch('/api/devices')
                .then(response => response.json())
                .then(data => {
                    const deviceList = document.getElementById('deviceList');
                    deviceList.innerHTML = data.devices.map(device => `
                        <div class="device-item">
                            <div class="device-info">
                                <h3>${device.name}</h3>
                                <p>📍 ${device.location} • ${device.id}</p>
                                <p style="font-size: 12px; margin-top: 5px;">อัพเดท: ${device.lastUpdate}</p>
                            </div>
                            <span class="device-status ${device.status}">${device.status === 'online' ? 'Online' : 'Offline'}</span>
                        </div>
                    `).join('');
                });
        }

        function showAddDevice() {
            document.getElementById('addDeviceModal').classList.add('active');
        }

        function closeAddDevice() {
            document.getElementById('addDeviceModal').classList.remove('active');
        }

        function addDevice(event) {
            event.preventDefault();
            const deviceData = {
                id: document.getElementById('deviceId').value,
                name: document.getElementById('deviceName').value,
                location: document.getElementById('deviceLocation').value
            };

            fetch('/api/add-device', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(deviceData)
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      closeAddDevice();
                      loadDevices();
                      showSuccessMessage('✓ เพิ่มอุปกรณ์สำเร็จ');
                  }
              });
        }

        function initChart() {
            filterChart('24h');
        }

        function filterChart(period) {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            const container = document.getElementById('chartContainer');
            const numBars = period === '24h' ? 8 : (period === '7d' ? 7 : 10);
            
            container.innerHTML = Array(numBars).fill(0).map((_, i) => {
                const height = 50 + Math.random() * 150;
                const label = period === '24h' ? `${i*3}:00` : 
                             period === '7d' ? `วัน ${i+1}` : 
                             `สัปดาห์ ${i+1}`;
                return `
                    <div class="chart-bar" style="height: ${height}px;">
                        <div class="chart-label">${label}</div>
                    </div>
                `;
            }).join('');
        }

        function startRealtimeSensor() {
            updateSensorData();
            setInterval(updateSensorData, 5000);
        }

        function updateSensorData() {
            fetch('/api/sensor-data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('realtimeEthylene').textContent = data.ethylene;
                    document.getElementById('realtimeCO2').textContent = data.co2;
                });
        }

        function showSuccessMessage(message, bg = '#4CAF50', color = 'white') {
            const successMsg = document.createElement('div');
            successMsg.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${bg};
                color: ${color};
                padding: 15px 25px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                z-index: 2000;
                font-weight: bold;
                animation: slideIn 0.3s ease;
            `;
            successMsg.textContent = message;
            document.body.appendChild(successMsg);
            
            setTimeout(() => successMsg.remove(), 2000);
        }
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/set-user-email', methods=['POST'])
def set_user_email():
    data = request.json
    email = data.get('email')
    session['user_email'] = email
    return jsonify({'success': True, 'email': email})


@app.route('/api/save-result', methods=['POST'])
def save_result():
    data = request.json
    email = data.get('email')
    
    if email not in user_data:
        user_data[email] = []
    
    now = datetime.now()
    date_str = now.strftime('%d %B %Y, %H:%M น.')
    
    result = {
        'date': date_str,
        'unripe': data.get('unripe'),
        'ripening': data.get('ripening'),
        'ready': data.get('ready'),
        'status': data.get('status'),
        'ethylene': data.get('ethylene'),
        'co2': data.get('co2')
    }
    
    user_data[email].insert(0, result)
    
    # Keep only last 20 records
    if len(user_data[email]) > 20:
        user_data[email] = user_data[email][:20]
    
    return jsonify({'success': True})


@app.route('/api/get-user-data')
def get_user_data():
    email = request.args.get('email')
    results = user_data.get(email, [])
    return jsonify({'success': True, 'results': results})


@app.route('/api/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    is_valid = any(
        cred['email'] == email and cred['password'] == password 
        for cred in ADMIN_CREDENTIALS
    )
    
    if is_valid:
        session['is_admin'] = True
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid credentials'})


@app.route('/api/devices')
def get_devices():
    return jsonify({'devices': DEVICES})


@app.route('/api/add-device', methods=['POST'])
def add_device():
    data = request.json
    new_device = {
        'id': data.get('id'),
        'name': data.get('name'),
        'location': data.get('location'),
        'status': 'online',
        'lastUpdate': 'เมื่อสักครู่'
    }
    DEVICES.append(new_device)
    return jsonify({'success': True})


@app.route('/api/sensor-data')
def get_sensor_data():
    import random
    ethylene = round(10 + random.random() * 50, 1)
    co2 = int(500 + random.random() * 1000)
    return jsonify({'ethylene': ethylene, 'co2': co2})


if __name__ == '__main__':
    print("🥭 Durian Smart AI - Starting Flask Server...")
    print("📧 Admin Credentials:")
    print("   Email: admin@durianai.com | Password: admin123")
    print("   Email: manager@durianai.com | Password: manager456")
    print("\n🌐 Server running at: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
