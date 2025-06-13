import { fetchWithAuth, handleResponse } from './fetchWithAuth.js'; 
const BASE_URL = import.meta.env.VITE_API_BASE_URL; 

export async function classifyImage(file) {
  console.log('[DEBUG] classifyImage: Called with file:', file ? file.name : 'None');
  const formData = new FormData();
  formData.append('image', file);

  try {
    
    const response = await fetchWithAuth('/predict/', {
      method: 'POST',
      body: formData
      
    });
    console.log('[DEBUG] classifyImage: Response status from fetchWithAuth /predict/:', response.status);
    const data = await handleResponse(response); 
    console.log('[DEBUG] classifyImage: Successfully classified. Returning data (raw):', data);
    console.log('[DEBUG] classifyImage: Successfully classified. Returning data (JSON):', JSON.stringify(data, null, 2));
    return data;

  } catch (err) {
    
    console.error('[DEBUG] classifyImage: Error during fetch/classification:', err.message); 
    throw err; 
  }
}


function displayClassificationResult(result) {
  console.log('[DEBUG] displayClassificationResult: Called with result (raw):', result);
  console.log('[DEBUG] displayClassificationResult: Called with result (JSON):', JSON.stringify(result, null, 2));
  document.querySelectorAll('.classification-result, .modal-backdrop').forEach(el => el.remove());
  
 let recommendedBanksHTML = '';
  if (result.recommended_banks && result.recommended_banks.length > 0) {
    recommendedBanksHTML = `
      <div style="margin-top: 15px;">
        <p><strong>Rekomendasi Bank Sampah Terdekat:</strong></p>
        <ul style="list-style-type: disc; padding-left: 20px; text-align: left;">
          ${result.recommended_banks.map(bank => `<li>${bank.name}</li>`).join('')}
        </ul>
      </div>
    `;
  } else {
    recommendedBanksHTML = '<p style="margin-top: 15px;">Tidak ada rekomendasi bank sampah terdekat.</p>';
  }

  const resultHTML = `
    <div class="classification-result" style="
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
      z-index: 1000;
      max-width: 450px;
      text-align: center;
      max-height: 90vh;
      overflow-y: auto;
    ">
      <h3 style="margin-bottom: 15px; color: #4caf50;">Hasil Klasifikasi</h3>
      <p><strong>Jenis Sampah:</strong> ${result.predicted_class || 'Tidak terdeteksi'}</p>

      <div style="margin: 20px 0; text-align: left;">
        <p><strong>Deskripsi:</strong> ${result.info && result.info.description ? result.info.description : 'Informasi tidak tersedia.'}</p>
        <p style="margin-top: 10px;"><strong>Cara Pengolahan:</strong> ${result.info && result.info.how_to_process ? result.info.how_to_process : 'Informasi tidak tersedia.'}</p>
      </div>

      ${recommendedBanksHTML}

      <button onclick="window.closeClassificationResult()" style="
        background-color: #4caf50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        cursor: pointer;
        margin-top: 20px;
      ">Tutup</button>
    </div>
    <div class="modal-backdrop" onclick="window.closeClassificationResult()" style="
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      z-index: 999;
    "></div>
  `;

  console.log('[DEBUG] displayClassificationResult: Generated HTML for modal (first 500 chars):', resultHTML.substring(0,500));
  console.log('[DEBUG] displayClassificationResult: Appending modal HTML to body.');
  document.body.insertAdjacentHTML('beforeend', resultHTML);
}


window.closeClassificationResult = function() {
  console.log('[DEBUG] closeClassificationResult: Called.');
  const resultModal = document.querySelector('.classification-result');
  const backdrop = document.querySelector('.modal-backdrop');
  if (resultModal) resultModal.remove();
  if (backdrop) backdrop.remove();
};


export async function handleClassification(selectedFile, submitBtnSelector = '.submit-btn') {
  console.log('[DEBUG] handleClassification (predict.js): Called with file:', selectedFile ? selectedFile.name : 'None', 'Button selector:', submitBtnSelector);
  if (!selectedFile) {
    alert('Mohon pilih gambar terlebih dahulu');
    return;
  }

  const submitBtn = document.querySelector(submitBtnSelector);
  let originalText = '';
  if (submitBtn) {
    originalText = submitBtn.textContent;
    submitBtn.textContent = 'Memproses...';
    submitBtn.disabled = true;
  }

  try {
    console.log('[DEBUG] handleClassification: Calling classifyImage...');
    const result = await classifyImage(selectedFile); 
    console.log('[DEBUG] handleClassification: Result from classifyImage (raw):', result);
    console.log('[DEBUG] handleClassification: Result from classifyImage (JSON):', JSON.stringify(result, null, 2));

    console.log('[DEBUG] handleClassification: Calling displayClassificationResult...');
    displayClassificationResult(result);
  } catch (error) {
    
    
    console.error('[DEBUG] handleClassification: Error during classification process:', error);
    alert('Terjadi kesalahan saat mengklasifikasi gambar: ' + error.message);
  } finally {
    if (submitBtn) {
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
    console.log('[DEBUG] handleClassification: Process finished, button state restored.');
  }
}
