import 'tag/timetable/timetable-month.tag';

<instrument>
  <h1>{ name }</h1>
  <p>{ remarks }</p>
  <timetable-month year={ year } month={ month } />

  <script>
    import * as riot from 'riot';
    import moment from 'moment';
    import { range } from 'js/utils/list.js';
    import { buildQueryParam } from 'js/utils/url.js';

    const now = moment();
    const url = `/api/instruments/${opts.pk}/`;

    let fetchInstrument = (year, month) => {
      let since = moment([year, month-1, 1, 0, 0, 0]);
      let until = moment(since).endOf('date').endOf('month');
      let param = buildQueryParam({
        since: since.format(),
        until: until.format(),
      });
      fetch(`${url}?${param}`)
        .then((data) => {
          return data.json();
        })
        .then((json) => {
          this.update({
            year: year,
            month: month,
            name: json.name,
            remarks: json.remarks,
            reservations: json.reservations,
          });
        });
    }

    riot.route('*/*', (year, month) => {
      fetchInstrument(
        parseInt(year)  || now.year(),
        parseInt(month) || now.month() + 1,
      );
    });
  </script>
</instrument>
