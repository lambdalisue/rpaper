import './record';

<reservations-filter-month>
  <div class="date" each={ date in dates }>
    <div class="hour" each={ hour in HOURS }></div>
  </div>
  <reservations-filter-month-record
    each={ record in state.thing.records.items }
    instance={ record }
    date_count={ dates.length }
    />

  <style scoped type='text/less'>
  :scope {
    display: block;
    position: relative;
    border: 1px solid #bbb;

    .date {
      display: flex;
      height: 2em;
      border-bottom: 1px dotted #aaa;
    }

    .hour {
      flex-grow: 1;
      border-right: 1px dotted #aaa;
      &:last-child {
        border-right: none;
      }
    }
  }
  </style>

  <script>
    import moment from 'moment';
    import { range } from 'ts/utils/list';
    import { FilterType, getFilterType } from 'ts/redux/reservations/utils/filter';

    this.HOURS = range(0, 24);

    this.on('update', () => {
      this.state = opts.state;
      if (getFilterType(this.state.thing.records.filter) === FilterType.MonthFilter) {
        let s = moment([
          this.state.thing.records.filter.year,
          this.state.thing.records.filter.month-1
        ]).startOf('month');
        let e = moment(s).endOf('month');
        this.dates = range(s.date(), e.date());
      }
    });
  </script>
</reservations-filter-month>
