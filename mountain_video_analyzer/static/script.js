document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const videoFile = document.getElementById('video-file');
    const uploadSection = document.getElementById('upload-section');
    const analysisSection = document.getElementById('analysis-section');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const progress = document.getElementById('progress');
    
    // アップロードフォームの送信
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!videoFile.files[0]) {
            alert('動画ファイルを選択してください');
            return;
        }
        
        // フォームデータの作成
        const formData = new FormData();
        formData.append('file', videoFile.files[0]);
        
        try {
            // アップロード中の表示
            uploadSection.style.display = 'none';
            analysisSection.style.display = 'block';
            loading.style.display = 'block';
            results.style.display = 'none';
            progress.textContent = 'アップロード中...';
            
            // ファイルのアップロード
            const uploadResponse = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!uploadResponse.ok) {
                throw new Error('アップロードに失敗しました');
            }
            
            const uploadData = await uploadResponse.json();
            progress.textContent = '分析中...';
            
            // 動画の分析
            const analyzeResponse = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `filepath=${encodeURIComponent(uploadData.filepath)}`
            });
            
            if (!analyzeResponse.ok) {
                throw new Error('分析に失敗しました');
            }
            
            const analysisData = await analyzeResponse.json();
            
            // 結果の表示
            loading.style.display = 'none';
            results.style.display = 'block';
            
            // 分析結果を表示
            displayResults(analysisData);
            
        } catch (error) {
            console.error('エラー:', error);
            alert(`エラーが発生しました: ${error.message}`);
            uploadSection.style.display = 'block';
            analysisSection.style.display = 'none';
        }
    });
    
    // 結果の表示関数
    function displayResults(data) {
        results.innerHTML = '';
        
        // データがない場合
        if (!data.scenes || data.scenes.length === 0) {
            results.innerHTML = '<p>シーンが検出されませんでした。</p>';
            return;
        }
        
        // ヘッダーの作成
        const header = document.createElement('div');
        header.innerHTML = `<h3>検出されたシーン: ${data.scenes.length}件</h3>`;
        results.appendChild(header);
        
        // シーンリストの作成
        const sceneList = document.createElement('div');
        sceneList.className = 'scene-list';
        
        data.scenes.forEach((scene, index) => {
            const sceneItem = document.createElement('div');
            sceneItem.className = 'scene-item';
            
            // 対応する説明を検索
            const description = data.descriptions.find(desc => desc.scene_id === scene.scene_id);
            const editingSuggestion = data.editing_suggestions.find(sugg => sugg.scene_id === scene.scene_id);
            
            // シーン情報を表示
            sceneItem.innerHTML = `
                <h4>シーン ${index + 1}</h4>
                <p><strong>開始時間:</strong> ${formatTime(scene.start_time)}</p>
                <p><strong>終了時間:</strong> ${formatTime(scene.end_time)}</p>
                ${description ? `<p><strong>説明:</strong> ${description.text}</p>` : ''}
                ${editingSuggestion ? `<p><strong>編集提案:</strong> ${editingSuggestion.text}</p>` : ''}
            `;
            
            sceneList.appendChild(sceneItem);
        });
        
        results.appendChild(sceneList);
    }
    
    // 時間のフォーマット（秒→MM:SS）
    function formatTime(seconds) {
        const min = Math.floor(seconds / 60);
        const sec = Math.floor(seconds % 60);
        return `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
    }
}); 