import './thing';
import './filter';
import './register';

<reservations-app>
  <reservations-register state={ state } />
  <reservations-thing state={ state } />
  <reservations-filter state={ state } />

  <script>
    import store from 'ts/redux/store';
    import moment from 'moment';
    import riot from 'riot';
    import { fetchThing, fetchRecords, setFilter } from 'ts/redux/reservations/actions';

    // Apply default values
    this.state = store.getState().reservations;

    store.subscribe(() => {
      const state = store.getState();
      const reservations = state.reservations;
      if (this.state !== reservations) {
        this.update({
          state: reservations,
        });
      }
    });

    this.on('mount', () => {
      store.dispatch(fetchThing({ pk: opts.pk }));
      store.dispatch(fetchRecords({
        pk: opts.pk,
        filter: this.state.thing.records.filter,
      }));
    });

    riot.route((year, month, date) => {
      store.dispatch(setFilter({
        year: year || undefined,
        month: month,
        date: date,
      }));
      store.dispatch(fetchRecords({
        pk: opts.pk,
        filter: this.state.thing.records.filter,
      }));
    });
  </script>
</reservations-app>
