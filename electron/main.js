const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { exec } = require('child_process');
const fs = require('fs');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    title: 'AI Intelligence Daily',
    icon: path.join(__dirname, 'build/icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // 尝试加载最新的报告
  const outputDir = path.join(__dirname, '..', 'output');
  const today = new Date().toISOString().split('T')[0];
  const reportPath = path.join(outputDir, `Daily_Report_${today}.html`);

  if (fs.existsSync(reportPath)) {
    mainWindow.loadFile(reportPath);
  } else {
    // 如果没有报告，加载欢迎页面
    mainWindow.loadFile(path.join(__dirname, 'welcome.html'));
  }

  // 开发模式下打开 DevTools
  // mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

// IPC: 运行数据获取
ipcMain.handle('run-fetch', async () => {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, '..', 'generate_report.py');
    exec(`python3 "${scriptPath}" --no-ai`, { cwd: path.join(__dirname, '..') }, (error, stdout, stderr) => {
      if (error) {
        reject({ error: error.message, stderr });
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
});

// IPC: 生成报告
ipcMain.handle('generate-report', async () => {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, '..', 'generate_browser_friendly.py');
    exec(`python3 "${scriptPath}"`, { cwd: path.join(__dirname, '..') }, (error, stdout, stderr) => {
      if (error) {
        reject({ error: error.message, stderr });
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
});

// IPC: 加载报告
ipcMain.handle('load-report', async () => {
  const outputDir = path.join(__dirname, '..', 'output');
  const today = new Date().toISOString().split('T')[0];
  const reportPath = path.join(outputDir, `Daily_Report_${today}.html`);

  if (fs.existsSync(reportPath)) {
    mainWindow.loadFile(reportPath);
    return { success: true, path: reportPath };
  } else {
    return { success: false, message: '今日报告尚未生成' };
  }
});

// IPC: 选择文件
ipcMain.handle('select-file', async (event, options) => {
  const result = await dialog.showOpenDialog(mainWindow, options);
  return result;
});
