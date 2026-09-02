document.addEventListener('DOMContentLoaded', function () {
  const select = document.getElementById('status-select');
  const badge = document.getElementById('status-badge');
  const statusText = document.getElementById('status-text');
  const message = document.getElementById('status-message');

  if (!select) return;

  select.addEventListener('change', function () {
    const newStatus = this.value;
    if (!newStatus) return;

    const studentId = this.dataset.studentId;

    fetch(`/students/${studentId}/status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus }),
    })
      .then(function (response) {
        if (!response.ok) throw new Error('Update failed');
        return response.json();
      })
      .then(function (data) {
        badge.textContent = data.status;
        badge.className = 'status-badge status-' + data.status;
        statusText.textContent = data.status;
        message.textContent = 'Status updated successfully.';
        message.className = 'status-message success';
      })
      .catch(function () {
        message.textContent = 'Could not update status. Please try again.';
        message.className = 'status-message error';
      });
  });
});
