const API_BASE_URL = 'http://localhost:8000';

async function getAllUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        const data = await response.json();
        const userList = document.getElementById('userList');

        let listHTML = '<div class="user-grid">';

        for (const [userId, user] of Object.entries(data)) {
            listHTML += `
                <div class="user-card">
                    <div class="user-info">
                        <i class="fas fa-user user-icon"></i>
                        <span class="user-id">${userId}</span>
                    </div>
                    <button onclick="redirectToDetail('${userId}')" class="detail-btn" aria-label="詳細を見る">
                        <span class="detail-text">詳細を見る</span>
                        <i class="fas fa-arrow-right"></i>
                    </button>
                </div>
            `;
        }

        listHTML += '</div>';
        userList.innerHTML = listHTML;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function getUser(specificUserId = null) {
    const userId = specificUserId || document.getElementById('userId').value;
    if (!userId) {
        alert('ユーザーIDを入力してください');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/${userId}`);
        const data = await response.json();
        const userDetails = document.getElementById('userDetails');
        const deleteButtonContainer = document.getElementById('deleteButtonContainer');

        if (data.error) {
            userDetails.innerHTML = `
                <div class="error-message">
                    <i class="fas fa-exclamation-circle"></i>
                    <h2>ユーザーが見つかりません</h2>
                </div>
            `;
            deleteButtonContainer.style.display = 'none';
            return;
        }
        
        let tableHTML = `
            <table border="1" style="width: 100%; border-collapse: collapse;">
                <tr>
                    <th style="padding: 8px;">ユーザーID</th>
                    <th style="padding: 8px;">First Name</th>
                    <th style="padding: 8px;">Last Name</th>
                    <th style="padding: 8px;">Born</th>
                </tr>
                <tr>
                    <td style="padding: 8px;">${userId}</td>
                    <td style="padding: 8px;">${data.first}</td>
                    <td style="padding: 8px;">${data.last}</td>
                    <td style="padding: 8px;">${data.born}</td>
                </tr>
            </table>
        `;
        
        userDetails.innerHTML = tableHTML;
        deleteButtonContainer.style.display = 'block';
    } catch (error) {
        const userDetails = document.getElementById('userDetails');
        const deleteButtonContainer = document.getElementById('deleteButtonContainer');
        userDetails.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-circle"></i>
                <h2>ユーザーが見つかりません</h2>
            </div>
        `;
        deleteButtonContainer.style.display = 'none';
        console.error('Error:', error);
    }
}

async function createUser() {
    const userId = document.getElementById('newUserId').value;
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const birthYear = document.getElementById('birthYear').value;

    if (!userId || !firstName || !lastName || !birthYear) {
        alert('すべての項目を入力してください');
        return;
    }

    const userData = {
        [userId]: {
            first: firstName,
            last: lastName,
            born: parseInt(birthYear)
        }
    };

    try {
        const response = await fetch(`${API_BASE_URL}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        const data = await response.json();
        alert('ユーザーが作成されました');
        getAllUsers();
    } catch (error) {
        console.error('Error:', error);
        alert('エラーが発生しました');
    }
}

// 詳細ページへの遷移関数を追加
function redirectToDetail(userId) {
    window.location.href = `user-detail.html?id=${userId}`;
}

// URLパラメータからユーザーIDを取得して詳細を表示する関数
function loadUserFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('id');
    if (userId) {
        // 検索フォームにユーザーIDを設定
        const userIdInput = document.getElementById('userId');
        if (userIdInput) {
            userIdInput.value = userId;
        }
        getUser(userId);
    }
}

// ナビゲーション読み込み用の関数
async function loadNavigation() {
    try {
        const response = await fetch('nav.html');
        if (!response.ok) throw new Error('Navigation load failed');
        
        const html = await response.text();
        
        // bodyの最初の要素としてナビゲーションを挿入
        document.body.insertAdjacentHTML('afterbegin', html);
        
        // 現在のページのナビゲーションアイテムをアクティブに設定
        setActiveNavItem();
    } catch (error) {
        console.error('Navigation loading error:', error);
        // エラー時のフォールバックナビゲーション
        provideFallbackNavigation();
    }
}

// 現在のページに基づいてナビゲーションアイテムをアクティブに設定
function setActiveNavItem() {
    // 現在のページのファイル名を取得（.htmlを除去）
    const currentPage = window.location.pathname.split('/').pop().replace('.html', '') || 'index';
    
    // 対応するナビゲーションアイテムを探してアクティブクラスを追加
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        if (item.dataset.page === currentPage) {
            item.classList.add('active');
        }
    });
}

// フォールバックナビゲーション（エラー時に表示）
function provideFallbackNavigation() {
    const fallbackNav = `
        <nav class="global-nav">
            <div class="nav-container">
                <a href="index.html" class="logo">
                    <i class="fas fa-cube logo-icon"></i>
                    <span class="logo-text">UMS</span>
                </a>
                <div class="nav-links">
                    <a href="index.html">ホーム</a>
                    <a href="user-list.html">ユーザー一覧</a>
                    <a href="user-detail.html">ユーザー詳細</a>
                    <a href="user-create.html">ユーザー登録</a>
                </div>
            </div>
        </nav>
    `;
    document.body.insertAdjacentHTML('afterbegin', fallbackNav);
}

// DOMContentLoadedイベントでナビゲーションを読み込む
document.addEventListener('DOMContentLoaded', loadNavigation); 