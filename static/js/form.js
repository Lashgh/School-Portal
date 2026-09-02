document.addEventListener('DOMContentLoaded', function () {
  const stateSelect = document.getElementById('state_of_origin');
  const lgaSelect = document.getElementById('local_government');

  if (!stateSelect || !lgaSelect) return;

  fetch('/static/data/states-lgas.json')
    .then(function (response) { return response.json(); })
    .then(function (stateInfo) {
      // Fill the State Of Origin select
      stateInfo.forEach(function (item) {
        stateSelect.appendChild(new Option(item.state, item.state));
      });

      // Repopulate Local Government when a State is selected
      stateSelect.addEventListener('change', function () {
        lgaSelect.innerHTML = '<option value="">Select-Local-Government</option>';
        const selected = stateInfo.find(function (item) { return item.state === stateSelect.value; });

        if (!selected) {
          lgaSelect.disabled = true;
          return;
        }

        selected.local.forEach(function (lga) {
          lgaSelect.appendChild(new Option(lga, lga));
        });
        lgaSelect.disabled = false;
      });
    })
    .catch(function (err) {
      console.error('Could not load states/LGA data:', err);
    });
});
