<reservation>
  A reservation by <span class="name">{ name }</span>
  from <time datetime="{ start_at }">{ start_at_display }</time>
  to <time datetime="{ end_at }">{ end_at_display }</time>

  <script>
  const url = `/api/instruments/${opts.instrument_pk}/reservations/${opts.pk}/`;
  fetch(url)
    .then((data) => {
      return data.json();
    })
    .then((json) => {
      this.name = json.name;
      this.start_at = json.start_at;
      this.start_at_display = json.start_at;
      this.end_at = json.end_at;
      this.end_at_display = json.end_at;
      this.update();
    });
  </script>
</reservation>
