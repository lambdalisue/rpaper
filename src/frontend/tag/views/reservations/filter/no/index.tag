import '../../record';

<reservations-filter-no>
  <h2>No filter</h2>

  <reservations-record instance={ record } each={ record in state.thing.records.items } />

  <script>
    this.on('update', () => {
      this.state = opts.state;
    });
  </script>
</reservations-filter-no>
