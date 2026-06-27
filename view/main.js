// view/main.js
// util phía frontend: gọi API backend, hiển thị toast, helper dùng chung
// tương tự Validation.java — nhưng chạy ở trình duyệt

// =============================
// CẤU HÌNH API BASE URL
// =============================
// Khi chạy local: "http://localhost:5000/api"
// Khi deploy lên Render: đổi thành URL của Render
// cùng server nên dùng đường dẫn tương đối, không cần ghi full URL
// khi deploy lên Render thì tự động đúng luôn, không cần sửa
const BASE_URL = "/api";

// =============================
// API HELPER
// tương tự các hàm static trong Validation.java
// =============================
const API = {
  // gọi GET request
  async get(path) {
    try {
      const res = await fetch(BASE_URL + path, {
        credentials: "include"  // gửi kèm cookie session
      });
      return await res.json();
    } catch (err) {
      console.error("GET error:", err);
      return { success: false, message: "Lỗi kết nối server" };
    }
  },

  // gọi POST request với body JSON
  async post(path, body) {
    try {
      const res = await fetch(BASE_URL + path, {
        method:      "POST",
        headers:     { "Content-Type": "application/json" },
        credentials: "include",
        body:        JSON.stringify(body)
      });
      return await res.json();
    } catch (err) {
      console.error("POST error:", err);
      return { success: false, message: "Lỗi kết nối server" };
    }
  },

  // gọi PUT request (cập nhật)
  async put(path, body) {
    try {
      const res = await fetch(BASE_URL + path, {
        method:      "PUT",
        headers:     { "Content-Type": "application/json" },
        credentials: "include",
        body:        JSON.stringify(body)
      });
      return await res.json();
    } catch (err) {
      console.error("PUT error:", err);
      return { success: false, message: "Lỗi kết nối server" };
    }
  },

  // gọi DELETE request
  async delete(path) {
    try {
      const res = await fetch(BASE_URL + path, {
        method:      "DELETE",
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
// hiển thị thông báo góc dưới phải
// =============================
let toastTimer = null;

function showToast(message, type = "default") {
  const toast = document.getElementById("toast");
  if (!toast) return;

  toast.textContent = message;
  toast.className   = "show " + type;  // "show success" | "show error" | "show"

  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.className = "";
  }, 2800);
}

// =============================
// MODAL HELPER
// =============================
function openModal(id)  {
  document.getElementById(id).classList.add("open");
}
function closeModal(id) {
  document.getElementById(id).classList.remove("open");
}

// =============================
// FORMAT TIỀN VIỆT NAM
// ví dụ: 15000000 → "15,000,000 ₫"
// =============================
function formatMoney(amount) {
  return Number(amount).toLocaleString("vi-VN") + " ₫";
}

// =============================
// FORMAT NGÀY
// "2025-06-15" → "15/06/2025"
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
    present:  ["badge-green",  "Có mặt"],
    absent:   ["badge-red",    "Vắng"],
    late:     ["badge-yellow", "Đi muộn"],
    approved: ["badge-green",  "Đã duyệt"],
    rejected: ["badge-red",    "Từ chối"],
    pending:  ["badge-yellow", "Chờ duyệt"],
  };
  const [cls, label] = map[status] || ["badge-gray", status];
  return `<span class="badge ${cls}">${label}</span>`;
}

// =============================
// KIỂM TRA ĐĂNG NHẬP
// gọi ở đầu mỗi trang (trừ index.html)
// nếu chưa đăng nhập → quay về trang login
// =============================
async function requireLogin() {
  const res = await API.get("/auth/me");
  if (!res.success) {
    window.location.href = "index.html";
    return null;
  }
  return res;  // trả về { employee_id, role, name }
}

// =============================
// RENDER SIDEBAR
// gọi sau requireLogin() để hiển thị menu
// =============================
function renderSidebar(currentPage, user) {
  const isAdmin = user.role === "admin";

  const adminLinks = isAdmin ? `
    <a class="nav-item ${currentPage === 'employees' ? 'active' : ''}" href="employees.html">
      <span class="icon">👥</span> Nhân viên
    </a>
  ` : "";

  document.getElementById("sidebar").innerHTML = `
    <div class="sidebar-logo">👔 Emp<span>Manager</span></div>

    <a class="nav-item ${currentPage === 'dashboard' ? 'active' : ''}" href="dashboard.html">
      <span class="icon">🏠</span> Tổng quan
    </a>
    <a class="nav-item ${currentPage === 'attendance' ? 'active' : ''}" href="attendance.html">
      <span class="icon">📋</span> Điểm danh
    </a>
    <a class="nav-item ${currentPage === 'leave' ? 'active' : ''}" href="leave.html">
      <span class="icon">🌴</span> Nghỉ phép
    </a>
    <a class="nav-item ${currentPage === 'salary' ? 'active' : ''}" href="salary.html">
      <span class="icon">💰</span> Lương thưởng
    </a>
    ${adminLinks}

    <div class="sidebar-bottom">
      <div style="padding:0 20px 8px;font-size:.8rem;color:#9ca3af;">
        Xin chào, <strong>${user.name}</strong>
        <span style="display:block;font-size:.75rem;margin-top:1px;">${isAdmin ? '🔑 Admin' : '👤 Nhân viên'}</span>
      </div>
      <button class="nav-item" onclick="doLogout()">
        <span class="icon">🚪</span> Đăng xuất
      </button>
    </div>
  `;
}

// xử lý đăng xuất
async function doLogout() {
  await API.post("/auth/logout", {});
  window.location.href = "index.html";
}
