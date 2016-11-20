import './no';
import './year';
import './month';
import './date';

<reservations-filter>
  <div class="info">
    <span class="year">{ state.filter.year }</span>
    <span class="month">{ state.filter.month }</span>
    <span class="date">{ state.filter.date }</span>
  </div>

  <reservations-filter-no state={ state } if={ filterType === FilterType.NoFilter } />
  <reservations-filter-year state={ state } if={ filterType === FilterType.YearFilter } />
  <reservations-filter-month state={ state } if={ filterType === FilterType.MonthFilter } />
  <reservations-filter-date state={ state } if={ filterType === FilterType.DateFilter } />

  <script>
    import { FilterType, getFilterType } from 'ts/redux/reservations/utils/filter';

    this.FilterType = FilterType;

    this.on('update', () => {
      this.state = opts.state;
      this.filterType = getFilterType(this.state.thing.records.filter);
    });
  </script>
</reservations-filter>
