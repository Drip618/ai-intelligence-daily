const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  runFetch: () => ipcRenderer.invoke('run-fetch'),
  generateReport: () => ipcRenderer.invoke('generate-report'),
  loadReport: () => ipcRenderer.invoke('load-report'),
  selectFile: (options) => ipcRenderer.invoke('select-file', options)
});
