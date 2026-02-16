import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าจอ
st.set_page_config(layout="wide", page_title="Durian Smart AI")

# --- ส่วนของโค้ด HTML/CSS/JS (อยู่ในเครื่องหมายคำพูด) ---
html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Durian Smart AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 700px; margin: 0 auto; position: relative; }
        
        /* Header */
        .header { text-align: center; margin-bottom: 30px; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .header h1 { color: #558B2F; font-size: 32px; margin-bottom: 10px; display: flex; align-items: center; justify-content: center; gap: 10px; }
        .header p { color: #F9A825; font-size: 16px; }
        .emoji { font-size: 40px; }
        .user-badge { background: #E8F5E9; color: #2E7D32; padding: 5px 15px; border-radius: 20px; font-size: 14px; margin-top: 10px; display: inline-block; }

        /* Mode Switch */
        .mode-switch { display: flex; gap: 10px; margin-bottom: 20px; background: white; padding: 10px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .mode-btn { flex: 1; padding: 15px; border: none; border-radius: 10px; cursor: pointer; font-size: 16px; font-weight: bold; transition: all 0.3s ease; background: #F5F5F5; color: #757575; }
        .mode-btn.active { background: linear-gradient(135deg, #81C784 0%, #AED581 100%); color: white; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
        .mode-btn.admin.active { background: linear-gradient(135deg, #FFF176 0%, #FFEB3B 100%); color: #558B2F; }

        .panel { display: none; }
        .panel.active { display: block; }
        
        /* User Panel Styles */
        .action-buttons { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        .action-btn { background: linear-gradient(135deg, #81C784 0%, #AED581 100%); border: none; padding: 20px; border-radius: 15px; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: white; font-size: 16px; font-weight: bold; display: flex; flex-direction: column; align-items: center; gap: 10px; }
        .action-btn:hover { transform: translateY(-3px); box-shadow: 0 6px 15px rgba(0,0,0,0.15); }
        .action-btn.yellow { background: linear-gradient(135deg, #FFF176 0%, #FFEB3B 100%); color: #558B2F; }
        .action-btn.data { grid-column: 1 / -1; background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%); }
        .icon { font-size: 40px; }

        .preview-area { background: white; border-radius: 20px; padding: 30px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); min-height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .preview-image { max-width: 100%; max-height: 300px; border-radius: 15px; margin-bottom: 20px; }
        
        .result-container { width: 100%; text-align: center; }
        .result-title { font-size: 24px; color: #558B2F; margin-bottom: 20px; font-weight: bold; }
        
        .ripeness-status { background: linear-gradient(135deg, #FFF176 0%, #FFEB3B 100%); color: #558B2F; padding: 20px; border-radius: 15px; margin-bottom: 20px; font-size: 24px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .ripeness-status.unripe { background: linear-gradient(135deg, #81C784 0%, #AED581 100%); color: white; }
        .ripeness-status.ripening { background: linear-gradient(135deg, #FFE082 0%, #FFD54F 100%); color: #F57F17; }
        .ripeness-status.ready { background: linear-gradient(135deg, #FFF176 0%, #FFEB3B 100%); color: #558B2F; }

        .ripeness-bars { display: flex; flex-direction: column; gap: 15px; margin-bottom: 20px; }
        .ripeness-item { text-align: left; }
        .ripeness-label { display: flex; justify-content: space-between; margin-bottom: 8px; font-weight: bold; color: #424242; }
        .ripeness-bar { background: #E0E0E0; height: 30px; border-radius: 15px; overflow: hidden; position: relative; }
        .ripeness-fill { height: 100%; border-radius: 15px; transition: width 1s ease; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }

        .sensor-data { background: #F1F8E9; padding: 15px; border-radius: 10px; margin-top: 15px; text-align: left; }
        .sensor-data h4 { color: #558B2F; margin-bottom: 10px; }
        .sensor-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #C5E1A5; }
        .sensor-item:last-child { border-bottom: none; }

        .placeholder { text-align: center; color: #9E9E9E; }
        .placeholder .icon { color: #C5E1A5; margin-bottom: 15px; }
        
        /* Admin Panel Styles */
        .admin-section { background: white; border-radius: 20px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .admin-section h3 { color: #558B2F; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
        
        .device-list { display: flex; flex-direction: column; gap: 15px; }
        .device-item { background: #F1F8E9; padding: 15px; border-radius: 10px; border-left: 4px solid #8BC34A; display: flex; justify-content: space-between; align-items: center; }
        .device-info h4 { color: #558B2F; margin-bottom: 5px; }
        .device-info p { color: #757575; font-size: 14px; }
        .device-status { padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .device-status.online { background: #C8E6C9; color: #2E7D32; }
        .device-status.offline { background: #FFCCBC; color: #D84315; }

        .add-device-btn { width: 100%; padding: 15px; background: linear-gradient(135deg, #FFF176 0%, #FFEB3B 100%); color: #558B2F; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; transition: all 0.3s ease; margin-top: 15px; }
        .add-device-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.15); }

        .gas-history-chart { background: #F9FBE7; padding: 20px; border-radius: 10px; margin-top: 15px; }
        .chart-row { display: flex; align-items: flex-end; gap: 10px; height: 150px; margin-top: 15px; }
        .chart-bar { flex: 1; background: linear-gradient(to top, #81C784, #AED581); border-radius: 5px 5px 0 0; position: relative; min-height: 20px; }
        .chart-label { position: absolute; bottom: -25px; left: 50%; transform: translateX(-50%); font-size: 11px; color: #757575; white-space: nowrap; }

        .filter-bar { display: flex; gap: 10px; margin-bottom: 15px; }
        .filter-btn { padding: 8px 15px; border: 2px solid #C5E1A5; background: white; border-radius: 8px; cursor: pointer; font-size: 14px; transition: all 0.3s ease; }
        .filter-btn.active { background: #81C784; color: white; border-color: #81C784; }

        /* Modal Styles */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; padding: 20px; }
        .modal.active { display: flex; align-items: center; justify-content: center; }
        .modal-content { background: white; border-radius: 20px; padding: 30px; max-width: 500px; width: 100%; max-height: 80vh; overflow-y: auto; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .modal-header h2 { color: #558B2F; }
        .close-btn { background: #FFEB3B; border: none; width: 35px; height: 35px; border-radius: 50%; cursor: pointer; font-size: 20px; color: #558B2F; font-weight: bold; }

        .data-list { display: flex; flex-direction: column; gap: 15px; }
        .data-item { background: #F1F8E9; padding: 15px; border-radius: 10px; border-left: 4px solid #8BC34A; }
        .data-item-date { font-size: 12px; color: #757575; margin-bottom: 5px; display: flex; justify-content: space-between;}
        .data-item-owner { font-weight: bold; color: #558B2F; }
        .data-item-result { font-weight: bold; color: #558B2F; margin-top: 5px; }

        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; color: #558B2F; font-weight: bold; margin-bottom: 8px; }
        .form-group input { width: 100%; padding: 12px; border: 2px solid #C5E1A5; border-radius: 8px; font-size: 14px; }
        .form-group input:focus { outline: none; border-color: #81C784; }
        .submit-btn { width: 100%; padding: 15px; background: linear-gradient(135deg, #81C784 0%, #AED581 100%); color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; }
        .logout-btn { background: #ef5350; margin-left: auto; font-size: 12px; padding: 5px 10px; color: white; border: none; border-radius: 5px; cursor: pointer;}

        /* Login Modal Specifics */
        .login-tabs { display: flex; margin-bottom: 20px; border-bottom: 2px solid #F1F8E9; }
        .login-tab { flex: 1; text-align: center; padding: 10px; cursor: pointer; color: #757575; font-weight: bold; }
        .login-tab.active { color: #558B2F; border-bottom: 3px solid #558B2F; }
        .login-form { display: none; }
        .login-form.active { display: block; }

        input[type="file"] { display: none; }
        .analyzing { color: #F9A825; font-size: 18px; margin-top: 20px; }
        .yolo-badge { display: inline-block; background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%); color: white; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-top: 10px; }
        .firebase-sync { display: flex; align-items: center; gap: 5px; justify-content: center; color: #F9A825; font-size: 14px; margin-top: 10px; }
        .sync-icon { animation: rotate 2s linear infinite; }
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><span class="emoji">🥭</span> Durian Smart AI</h1>
            <p>ระบบวิเคราะห์ทุเรียนอัจฉริยะ</p>
            <div id="userInfo" style="display: none;">
                <span class="user-badge" id="userEmailDisplay"></span>
                <button class="logout-btn" onclick="logout()">ออกจากระบบ</button>
            </div>
        </div>

        <div class="mode-switch">
            <button class="mode-btn active" onclick="switchModeRequest('user')">👤 ผู้ใช้งาน</button>
            <button class="mode-btn admin" onclick="switchModeRequest('admin')">🔧 ผู้ดูแลระบบ</button>
        </div>

        <div class="panel active" id="userPanel">
            <div class="action-buttons">
                <button class="action-btn" onclick="openCamera()">
                    <span class="icon">📷</span><span>ถ่ายภาพ</span>
                </button>
                <button class="action-btn yellow" onclick="scanImage()">
                    <span class="icon">🔍</span><span>แสกน</span>
                </button>
                <button class="action-btn" onclick="uploadImage()">
                    <span class="icon">🖼️</span><span>เพิ่มรูป</span>
                </button>
                <button class="action-btn data" onclick="showData()">
                    <span class="icon">📊</span><span>ดูข้อมูลของฉัน</span>
                </button>
            </div>

            <div class="preview-area" id="previewArea">
                <div class="placeholder">
                    <div class="icon">🥭</div>
                    <p>ยินดีต้อนรับ! เลือกการทำงานด้านบน</p>
                    <div class="yolo-badge">✨ วิเคราะห์ด้วย YOLO Model</div>
                </div>
            </div>
        </div>

        <div class="panel" id="adminPanel">
            <div class="admin-section">
                <h3>📱 จัดการอุปกรณ์ (Device Management)</h3>
                <div class="device-list" id="deviceList">
                    </div>
                <button class="add-device-btn" onclick="showAddDevice()">➕ เพิ่มอุปกรณ์ใหม่</button>
            </div>

            <div class="admin-section">
                <h3>📈 ประวัติค่าการอ่านก๊าซ (Gas Sensor History)</h3>
                <div class="filter-bar">
                    <button class="filter-btn active" onclick="filterGasData('24h')">24 ชั่วโมง</button>
                    <button class="filter-btn" onclick="filterGasData('7d')">7 วัน</button>
                    <button class="filter-btn" onclick="filterGasData('30d')">30 วัน</button>
                </div>
                <div class="gas-history-chart">
                    <h4 style="color: #558B2F; margin-bottom: 10px;">ค่าเฉลี่ยการอ่านก๊าซ (ppm)</h4>
                    <div class="chart-row" id="gasChart">
                        </div>
                </div>
                <div class="sensor-data" style="margin-top: 20px;">
                    <h4>ข้อมูลเซนเซอร์ล่าสุด</h4>
                    <div class="sensor-item">
                        <span>อุปกรณ์:</span><strong id="currentDevice">DEVICE-001</strong>
                    </div>
                    <div class="sensor-item">
                        <span>ค่าก๊าซเอทิลีน:</span><strong id="ethyleneValue">-</strong>
                    </div>
                    <div class="sensor-item">
                        <span>ค่าก๊าซ CO2:</span><strong id="co2Value">-</strong>
                    </div>
                    <div class="sensor-item">
                        <span>สถานะเซนเซอร์:</span><strong id="sensorStatus" style="color: #4CAF50;">เสถียร</strong>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="modal active" id="loginModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>🔐 เข้าสู่ระบบ</h2>
            </div>
            
            <div class="login-tabs">
                <div class="login-tab active" onclick="switchLoginTab('user')">ผู้ใช้งานทั่วไป</div>
                <div class="login-tab" onclick="switchLoginTab('admin')">ผู้ดูแลระบบ</div>
            </div>

            <form id="userLoginForm" class="login-form active" onsubmit="handleUserLogin(event)">
                <p style="margin-bottom: 15px; color: #757575;">กรุณาระบุอีเมลเพื่อใช้บันทึกประวัติการสแกนของคุณ</p>
                <div class="form-group">
                    <label>อีเมลผู้ใช้งาน:</label>
                    <input type="email" id="userEmailInput" placeholder="name@example.com" required>
                </div>
                <button type="submit" class="submit-btn">เข้าใช้งาน</button>
            </form>

            <form id="adminLoginForm" class="login-form" onsubmit="handleAdminLogin(event)">
                <div class="form-group">
                    <label>อีเมล Admin:</label>
                    <input type="email" id="adminEmailInput" placeholder="admin@durian.com" required>
                </div>
                <div class="form-group">
                    <label>รหัสผ่าน:</label>
                    <input type="password" id="adminPasswordInput" placeholder="รหัสผ่าน" required>
                </div>
                <p style="font-size: 12px; color: #ef5350; margin-bottom: 10px; display: none;" id="adminLoginError">อีเมลหรือรหัสผ่านไม่ถูกต้อง</p>
                <button type="submit" class="submit-btn yellow">เข้าสู่ระบบ Admin</button>
            </form>
        </div>
    </div>

    <div class="modal" id="dataModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>📊 ประวัติการวิเคราะห์</h2>
                <button class="close-btn" onclick="closeData()">×</button>
            </div>
            <div class="data-list" id="dataList">
                </div>
        </div>
    </div>

    <div class="modal" id="addDeviceModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>➕ เพิ่มอุปกรณ์ใหม่</h2>
                <button class="close-btn" onclick="closeAddDevice()">×</button>
            </div>
            <form onsubmit="addDevice(event)">
                <div class="form-group">
                    <label>Device ID:</label>
                    <input type="text" id="deviceId" placeholder="เช่น DEVICE-005" required>
                </div>
                <div class="form-group">
                    <label>ชื่ออุปกรณ์:</label>
                    <input type="text" id="deviceName" placeholder="เช่น เซนเซอร์ทุเรียน A" required>
                </div>
                <div class="form-group">
                    <label>สถานที่ติดตั้ง:</label>
                    <input type="text" id="deviceLocation" placeholder="เช่น โกดัง A1" required>
                </div>
                <button type="submit" class="submit-btn">เพิ่มอุปกรณ์</button>
            </form>
        </div>
    </div>

    <input type="file" id="fileInput" accept="image/*" onchange="handleFile(event)">
    <input type="file" id="cameraInput" accept="image/*" capture="environment" onchange="handleFile(event)">

    <script>
        // Sample data
        let devices = [
            { id: 'DEVICE-001', name: 'เซนเซอร์ทุเรียน A', location: 'โกดัง A1', status: 'online', lastUpdate: '2 นาทีที่แล้ว' },
            { id: 'DEVICE-002', name: 'เซนเซอร์ทุเรียน B', location: 'โกดัง A2', status: 'online', lastUpdate: '5 นาทีที่แล้ว' },
            { id: 'DEVICE-003', name: 'เซนเซอร์ทุเรียน C', location: 'โกดัง B1', status: 'offline', lastUpdate: '2 ชั่วโมงที่แล้ว' },
            { id: 'DEVICE-004', name: 'เซนเซอร์ทุเรียน D', location: 'โกดัง B2', status: 'online', lastUpdate: '1 นาทีที่แล้ว' }
        ];

        let savedData = [];
        let currentUser = null; // Stores email of current user
        let isAdmin = false;

        // Initialize
        window.onload = function() {
            // Show Login Modal by default is already handled by HTML class 'active'
            renderDevices();
            generateGasChart('24h');
            updateSensorData();
        };

        // --- Login System ---
        function switchLoginTab(type) {
            document.querySelectorAll('.login-tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.login-form').forEach(form => form.classList.remove('active'));
            
            if (type === 'user') {
                document.querySelectorAll('.login-tab')[0].classList.add('active');
                document.getElementById('userLoginForm').classList.add('active');
            } else {
                document.querySelectorAll('.login-tab')[1].classList.add('active');
                document.getElementById('adminLoginForm').classList.add('active');
            }
        }

        function handleUserLogin(e) {
            e.preventDefault();
            const email = document.getElementById('userEmailInput').value;
            if (email) {
                currentUser = email;
                isAdmin = false;
                loginSuccess('user');
            }
        }

        function handleAdminLogin(e) {
            e.preventDefault();
            const email = document.getElementById('adminEmailInput').value;
            const password = document.getElementById('adminPasswordInput').value;
            
            // Hardcoded Admin Credentials for Demo
            if (email === 'admin@durian.com' && password === '1234') {
                currentUser = email;
                isAdmin = true;
                loginSuccess('admin');
            } else {
                document.getElementById('adminLoginError').style.display = 'block';
            }
        }

        function loginSuccess(role) {
            document.getElementById('loginModal').classList.remove('active');
            document.getElementById('userInfo').style.display = 'block';
            document.getElementById('userEmailDisplay').textContent = isAdmin ? '🔧 Admin: ' + currentUser : '👤 ' + currentUser;
            
            if (role === 'admin') {
                switchMode('admin');
            } else {
                switchMode('user');
            }
        }

        function logout() {
            currentUser = null;
            isAdmin = false;
            document.getElementById('userInfo').style.display = 'none';
            document.getElementById('loginModal').classList.add('active');
            // Reset forms
            document.getElementById('userLoginForm').reset();
            document.getElementById('adminLoginForm').reset();
            document.getElementById('adminLoginError').style.display = 'none';
            switchLoginTab('user'); // Reset to user tab
        }

        // --- Mode Switching ---
        function switchModeRequest(mode) {
            if (!currentUser) {
                document.getElementById('loginModal').classList.add('active');
                return;
            }
            
            if (mode === 'admin' && !isAdmin) {
                alert('🚫 คุณไม่มีสิทธิ์เข้าถึงส่วน Admin (ต้องล็อกอินด้วยบัญชีแอดมิน)');
                // Optionally verify admin again or just block
                return;
            }
            switchMode(mode);
        }

        function switchMode(mode) {
            document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
            if (mode === 'user') document.querySelector('.mode-btn:first-child').classList.add('active');
            if (mode === 'admin') document.querySelector('.mode-btn.admin').classList.add('active');
            
            document.querySelectorAll('.panel').forEach(panel => panel.classList.remove('active'));
            document.getElementById(mode + 'Panel').classList.add('active');
        }

        // --- User Panel Functions ---
        function openCamera() { document.getElementById('cameraInput').click(); }
        function scanImage() { document.getElementById('fileInput').click(); }
        function uploadImage() { document.getElementById('fileInput').click(); }

        function handleFile(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    showAnalyzing(e.target.result);
                    setTimeout(() => analyzeImage(e.target.result), 2000);
                };
                reader.readAsDataURL(file);
            }
        }

        function showAnalyzing(imageSrc) {
            const previewArea = document.getElementById('previewArea');
            previewArea.innerHTML = `
                <img src="${imageSrc}" class="preview-image" alt="Durian">
                <div class="analyzing">🔄 กำลังวิเคราะห์ด้วย YOLO...</div>
                <div class="firebase-sync">
                    <span class="sync-icon">🔄</span>
                    <span>กำลังบันทึกข้อมูลไปยังบัญชี: ${currentUser}</span>
                </div>
            `;
        }

        function analyzeImage(imageSrc) {
            const rand = Math.random();
            let unripePercent, ripeningPercent, readyPercent, status, statusClass;

            if (rand < 0.33) {
                unripePercent = Math.floor(Math.random() * 20) + 70;
                ripeningPercent = Math.floor(Math.random() * 15) + 5;
                readyPercent = 100 - unripePercent - ripeningPercent;
                status = '🟢 ดิบ (Unripe)';
                statusClass = 'unripe';
            } else if (rand < 0.66) {
                unripePercent = Math.floor(Math.random() * 20) + 10;
                ripeningPercent = Math.floor(Math.random() * 20) + 50;
                readyPercent = 100 - unripePercent - ripeningPercent;
                status = '🟡 เริ่มสุก (Ripening)';
                statusClass = 'ripening';
            } else {
                unripePercent = Math.floor(Math.random() * 10) + 5;
                ripeningPercent = Math.floor(Math.random() * 20) + 10;
                readyPercent = 100 - unripePercent - ripeningPercent;
                status = '🟡 สุกพร้อมรับประทาน (Ready to Eat)';
                statusClass = 'ready';
            }

            const ethylene = (Math.random() * 50 + 10).toFixed(2);
            const co2 = (Math.random() * 1000 + 500).toFixed(2);

            const previewArea = document.getElementById('previewArea');
            previewArea.innerHTML = `
                <img src="${imageSrc}" class="preview-image" alt="Durian">
                <div class="result-container">
                    <div class="result-title">✨ ผลการวิเคราะห์</div>
                    <div class="ripeness-status ${statusClass}">${status}</div>
                    <div class="ripeness-bars">
                        <div class="ripeness-item">
                            <div class="ripeness-label"><span>🟢 ทุเรียนดิบ</span><span>${unripePercent}%</span></div>
                            <div class="ripeness-bar"><div class="ripeness-fill" style="width: ${unripePercent}%; background: linear-gradient(90deg, #81C784 0%, #66BB6A 100%);">${unripePercent}%</div></div>
                        </div>
                        <div class="ripeness-item">
                            <div class="ripeness-label"><span>🟠 ทุเรียนเริ่มสุก</span><span>${ripeningPercent}%</span></div>
                            <div class="ripeness-bar"><div class="ripeness-fill" style="width: ${ripeningPercent}%; background: linear-gradient(90deg, #FFE082 0%, #FFD54F 100%);">${ripeningPercent}%</div></div>
                        </div>
                        <div class="ripeness-item">
                            <div class="ripeness-label"><span>🟡 ทุเรียนสุกพร้อมรับประทาน</span><span>${readyPercent}%</span></div>
                            <div class="ripeness-bar"><div class="ripeness-fill" style="width: ${readyPercent}%; background: linear-gradient(90deg, #FFF176 0%, #FFEB3B 100%);">${readyPercent}%</div></div>
                        </div>
                    </div>
                    <div class="sensor-data">
                        <h4>📊 ข้อมูลจากเซนเซอร์ก๊าซ</h4>
                        <div class="sensor-item"><span>Ethylene (C₂H₄):</span><strong>${ethylene} ppm</strong></div>
                        <div class="sensor-item"><span>Carbon Dioxide (CO₂):</span><strong>${co2} ppm</strong></div>
                    </div>
                    <div class="yolo-badge">✨ บันทึกข้อมูลของ: ${currentUser}</div>
                </div>
            `;
            saveResult(unripePercent, ripeningPercent, readyPercent, status, ethylene, co2);
        }

        function saveResult(unripe, ripening, ready, status, ethylene, co2) {
            const now = new Date();
            const dateStr = now.toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });
            
            // Save with OWNER email
            savedData.unshift({ 
                owner: currentUser, // Important: save who owns this data
                date: dateStr, 
                unripe: unripe, 
                ripening: ripening, 
                ready: ready, 
                status: status, 
                ethylene: ethylene, 
                co2: co2 
            });
            
            if (savedData.length > 50) savedData.pop();
        }

        function showData() {
            const dataList = document.getElementById('dataList');
            // Filter data only for CURRENT USER
            const myData = savedData.filter(item => item.owner === currentUser);

            if (myData.length === 0) {
                dataList.innerHTML = `<div style="text-align: center; padding: 40px; color: #9E9E9E;"><div style="font-size: 48px; margin-bottom: 15px;">📭</div><p>ยังไม่มีข้อมูลของคุณ (${currentUser})</p></div>`;
            } else {
                dataList.innerHTML = myData.map(item => `
                    <div class="data-item">
                        <div class="data-item-date"><span>${item.date}</span></div>
                        <div class="data-item-result">${item.status}</div>
                        <div style="font-size: 13px; color: #757575; margin-top: 8px;">ดิบ: ${item.unripe}% | เริ่มสุก: ${item.ripening}% | สุก: ${item.ready}%</div>
                        <div style="font-size: 13px; color: #757575; margin-top: 5px;">Ethylene: ${item.ethylene} ppm | CO₂: ${item.co2} ppm</div>
                    </div>
                `).join('');
            }
            document.getElementById('dataModal').classList.add('active');
        }

        function closeData() {
            document.getElementById('dataModal').classList.remove('active');
        }

        // --- Admin Panel Functions ---
        function renderDevices() {
            const deviceList = document.getElementById('deviceList');
            deviceList.innerHTML = devices.map(device => `
                <div class="device-item">
                    <div class="device-info">
                        <h4>${device.id}</h4>
                        <p>📍 ${device.location} • อัปเดตล่าสุด: ${device.lastUpdate}</p>
                    </div>
                    <div class="device-status ${device.status}">${device.status === 'online' ? '🟢 ออนไลน์' : '🔴 ออฟไลน์'}</div>
                </div>
            `).join('');
        }

        function showAddDevice() { document.getElementById('addDeviceModal').classList.add('active'); }
        function closeAddDevice() { document.getElementById('addDeviceModal').classList.remove('active'); }

        function addDevice(event) {
            event.preventDefault();
            const deviceId = document.getElementById('deviceId').value;
            const deviceName = document.getElementById('deviceName').value;
            const deviceLocation = document.getElementById('deviceLocation').value;
            devices.push({ id: deviceId, name: deviceName, location: deviceLocation, status: 'online', lastUpdate: 'เพิ่งเพิ่ม' });
            renderDevices();
            closeAddDevice();
            event.target.reset();
        }

        function generateGasChart(period) {
            const chart = document.getElementById('gasChart');
            let labels;
            if (period === '24h') labels = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'];
            else if (period === '7d') labels = ['จ.', 'อ.', 'พ.', 'พฤ.', 'ศ.', 'ส.', 'อา.'];
            else labels = ['สัปดาห์ 1', 'สัปดาห์ 2', 'สัปดาห์ 3', 'สัปดาห์ 4'];

            chart.innerHTML = labels.map(label => {
                const height = Math.random() * 80 + 20;
                return `<div class="chart-bar" style="height: ${height}%"><div class="chart-label">${label}</div></div>`;
            }).join('');
        }

        function filterGasData(period) {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            generateGasChart(period);
        }

        function updateSensorData() {
            const ethylene = (Math.random() * 50 + 10).toFixed(2);
            const co2 = (Math.random() * 1000 + 500).toFixed(2);
            document.getElementById('ethyleneValue').textContent = ethylene + ' ppm';
            document.getElementById('co2Value').textContent = co2 + ' ppm';
            setTimeout(updateSensorData, 5000);
        }

        // Close modals when clicking outside
        document.getElementById('dataModal').addEventListener('click', function(e) { if (e.target === this) closeData(); });
        document.getElementById('addDeviceModal').addEventListener('click', function(e) { if (e.target === this) closeAddDevice(); });
    </script>
</body>
</html>
"""

# --- ส่วนสั่งแสดงผลของ Streamlit (ดึงตัวแปร html_code มาโชว์) ---
components.html(html_code, height=900, scrolling=True)





