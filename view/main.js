// view/main.js
// util phía frontend: gọi API backend, hiển thị toast, helper dùng chung
// tương tự Validation.java — nhưng chạy ở trình duyệt

// =============================
// CẤU HÌNH API BASE URL
// =============================
const BASE_URL = "/api";

// =============================
// API HELPER
// =============================
const API = {
  async get(path) {
    try {
      const res = await fetch(BASE_URL + path, {
        credentials: "include"
      });
      return await res.json();
    } catch (err) {
      console.error("GET error:", err);
      return { success: false, message: "Lỗi kết nối server" };
    }
  },

  async post(path, body) {
    try {
      const res = await fetch(BASE_URL + path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(body)
      });
      return await res.json();
    } catch (err) {
      console.error("POST error:", err);
      return { success: false, message: "Lỗi kết nối server" };
    }
  },

  async put(path, body) {
    try {
      const res = await fetch(BASE_URL + path, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(body)
      });
      return await res.json();
    } catch (err) {
      console.error("PUT error:", err);
      return { success: false, message: "Lỗi kết nối server" };
    }
  },

  async delete(path) {
    try {
      const res = await fetch(BASE_URL + path, {
        method: "DELETE",
        credentials: "include"
      });
      return await res.json();
    } catch (err) {
      console.error("DELETE error:", err);
      return { success: false, message: "Lỗi kết nối server" };
    }
  }
};

// =============================
// TOAST NOTIFICATION
// =============================
let toastTimer = null;

function showToast(message, type = "default") {
  const toast = document.getElementById("toast");
  if (!toast) return;

  toast.textContent = message;
  toast.className = "show " + type;

  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.className = "";
  }, 3000);
}

// =============================
// MODAL HELPER
// =============================
function openModal(id) {
  document.getElementById(id).classList.add("open");
}

function closeModal(id) {
  document.getElementById(id).classList.remove("open");
}

// =============================
// FORMAT TIỀN VIỆT NAM
// =============================
function formatMoney(amount) {
  return Number(amount).toLocaleString("vi-VN") + " ₫";
}

// =============================
// FORMAT NGÀY
// =============================
function formatDate(dateStr) {
  if (!dateStr) return "—";
  const [y, m, d] = dateStr.split("-");
  return `${d}/${m}/${y}`;
}

// =============================
// BADGE HTML HELPER
// =============================
function badgeStatus(status) {
  const map = {
    present: ["badge-green", "Có mặt"],
    absent: ["badge-red", "Vắng"],
    late: ["badge-yellow", "Đi muộn"],
    approved: ["badge-green", "Đã duyệt"],
    rejected: ["badge-red", "Từ chối"],
    pending: ["badge-yellow", "Chờ duyệt"],
  };

  const [cls, label] = map[status] || ["badge-gray", status];
  return `<span class="badge ${cls}">${label}</span>`;
}

// =============================
// KIỂM TRA ĐĂNG NHẬP
// =============================
async function requireLogin() {
  const res = await API.get("/auth/me");

  if (!res.success) {
    window.location.href = "index.html";
    return null;
  }

  return res;
}

// =============================
// LẤY AVATAR CỦA NGƯỜI DÙNG
// =============================
let cachedAvatar = null;
let avatarLoading = false;

async function getUserAvatar() {
  if (cachedAvatar !== null) {
    return cachedAvatar;
  }

  if (avatarLoading) {
    return new Promise((resolve) => {
      const checkCache = setInterval(() => {
        if (!avatarLoading) {
          clearInterval(checkCache);
          resolve(cachedAvatar);
        }
      }, 100);
    });
  }

  avatarLoading = true;
  try {
    const res = await API.get("/auth/profile");
    if (res.success && res.data && res.data.avatar) {
      cachedAvatar = res.data.avatar;
    } else {
      cachedAvatar = null;
    }
  } catch (err) {
    console.error("Lỗi lấy avatar:", err);
    cachedAvatar = null;
  } finally {
    avatarLoading = false;
  }

  return cachedAvatar;
}

// =============================
// RENDER SIDEBAR
// =============================
function renderSidebar(currentPage, user) {
  const isAdmin = user.role === "admin";

  const adminLinks = isAdmin ? `
    <a class="nav-item ${currentPage === 'employees' ? 'active' : ''}" href="employees.html">
      <img src="image/logo_quan_li_nhan_vien.png" style="height:18px;width:18px;object-fit:contain;" />
      HR
    </a>
    <a class="nav-item ${currentPage === 'assets' ? 'active' : ''}" href="assets.html">
      <img src="image/logo_tai_san.png" style="height:18px;width:18px;object-fit:contain;" />
      Tài sản
    </a>
    <a class="nav-item ${currentPage === 'risks' ? 'active' : ''}" href="risks.html">
      <img src="image/logo_rui_ro.png" style="height:18px;width:18px;object-fit:contain;" />
      Rủi ro
    </a>
    <a class="nav-item ${currentPage === 'incidents' ? 'active' : ''}" href="incidents.html">
      <img src="image/logo_su_co.png" style="height:18px;width:18px;object-fit:contain;" />
      Sự cố
    </a>
  ` : "";

  document.getElementById("sidebar").innerHTML = `
    <div class="sidebar-logo">
      <img src="image/logo_E.png" style="height:22px;vertical-align:middle;margin-right:6px;" />
      Smart<span>EMS</span>
    </div>

    <a class="nav-item ${currentPage === 'dashboard' ? 'active' : ''}" href="dashboard.html">
      <img src="image/logo_ngoi_nha.png" style="height:18px;width:18px;object-fit:contain;" />
      Home
    </a>

    <a class="nav-item ${currentPage === 'attendance' ? 'active' : ''}" href="attendance.html">
      <img src="image/logo_diem_danh.png" style="height:18px;width:18px;object-fit:contain;" />
      Điểm danh
    </a>

    <a class="nav-item ${currentPage === 'leave' ? 'active' : ''}" href="leave.html">
      <img src="image/logo_nghi_phep.png" style="height:18px;width:18px;object-fit:contain;" />
      Nghỉ phép
    </a>

    <a class="nav-item ${currentPage === 'salary' ? 'active' : ''}" href="salary.html">
      <img src="image/logo_luong.png" style="height:18px;width:18px;object-fit:contain;" />
      Lương thưởng
    </a>

    ${adminLinks}

    <div class="sidebar-bottom">
      <a class="nav-item ${currentPage === 'profile' ? 'active' : ''}" href="profile.html" style="margin-bottom:4px;">
        <span class="profile-avatar-container">
          <img src="image/logo_profile_co_ban.png" style="width:20px;height:20px;border-radius:50%;object-fit:cover;border:1.5px solid var(--border);" id="sidebar-avatar" />
        </span>
        Profile
      </a>
      <button class="nav-item" onclick="doLogout()">
        <img src="image/logo_dang_xuat.png" style="height:18px;width:18px;object-fit:contain;" />
        Đăng xuất
      </button>
    </div>
  `;

  getUserAvatar().then(avatar => {
    const sidebar = document.getElementById("sidebar");
    if (!sidebar) return;

    const avatarImg = sidebar.querySelector('#sidebar-avatar');
    if (avatarImg && avatar) {
      avatarImg.src = avatar;
    }
  });
}

// =============================
// XỬ LÝ ĐĂNG XUẤT
// =============================
async function doLogout() {
  await API.post("/auth/logout", {});
  cachedAvatar = null;
  window.location.href = "index.html";
}

// =============================
// HÀM LÀM MỚI AVATAR TRÊN SIDEBAR
// =============================
function refreshSidebarAvatar() {
  cachedAvatar = null;
  const currentPage = window.location.pathname.split('/').pop().replace('.html', '') || 'dashboard';
  API.get("/auth/me").then(res => {
    if (res.success) {
      renderSidebar(currentPage, res);
    }
  });
}