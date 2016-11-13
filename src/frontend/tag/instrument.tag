import './reservation.tag';

<instrument>
  <h1>{ name }</h1>
  <p>{ remarks }</p>
  <ul>
    <li each={ reservations }>
      <reservation
        instrument_pk="{ instrument }"
        pk="{ pk }">
      </reservation>
    </li>
  </ul>

  <script>
  const url = `/api/instruments/${opts.pk}/`;
  fetch(url)
    .then((data) => {
      return data.json();
    })
    .then((json) => {
      this.name = json.name;
      this.remarks = json.remarks;
      this.instrument_pk = json.pk;
      this.reservations = json.reservations;
      this.update();
    });
  </script>
</instrument>
