<timetable-month>
  <span class="year">{ year }</span>
  <span class="month">{ month }</span>
  <div class="dates">
    <div class="date" each={ date in dates }>
      <span>{ date }</span>
      <div class="hour" each={ hour in hours }></div>
    </div>
  </div>

  <style scoped type='text/less'>
  .date {
    display: flex;
    border-bottom: 1px solid #bbb;

    &:first-child {
      border-top: 1px solid #bbb;
    }

    & > span {
      display: block;
      width: 3em;
      text-align: center;
      vertical-align: middle;
      border-right: 1px solid #aaa;
    }

    & > .hour {
      flex-grow: 1;
      border-right: 1px dotted #aaa;
      &:last-child {
        border-right: 1px solid #aaa;
      }
    }
  }
  </style>

  <script>
    import moment from 'moment';
    import { range } from 'js/utils/list.js';

    const now  = Object.freeze(moment());
    this.hours = Object.freeze(range(0, 24));
    this.year  = opts.year  || now.year();
    this.month = opts.month || (now.month() + 1);

    this.on('update', (event) => {
      this.year  = opts.year  || this.year;
      this.month = opts.month || this.month;
      let s = moment([this.year, this.month-1]);
      let e = moment(s).endOf('month');
      this.dates = range(s.date(), e.date());
    });
  </script>
</timetable-month>
