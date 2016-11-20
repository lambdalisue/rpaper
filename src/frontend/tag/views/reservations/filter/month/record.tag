import '../../record';

<reservations-filter-month-record>
  <reservations-record class="primary" instance={ instance } />
  <reservations-record class="secondary" instance={ instance } if={ is_separated } />

  <style scoped type="text/less">
  reservations-record {
    display: block;
    position: absolute;
  }
  </style>

  <script>
    import moment from 'moment';

    let applyCoordinateExpressions = (element, s, e) => {
      let a = moment(s).startOf('date');
      let n = this.date_count;
      element.style.top = `calc(100% / ${n} * ${s.date()})`;
      element.style.left = `calc(100% / 24 / 60 * ${s.diff(a, 'minutes')})`;
      element.style.width = `calc(100% / 24 / 60 * ${e.diff(s, 'minutes')})`;
      element.style.height = `calc(100% / ${n})`;
    };

    this.on('update', () => {
      this.instance = opts.instance;
      this.date_count = opts.date_count;
      this.is_separated = this.instance.start_at.date() !== this.instance.end_at.date();
    });

    this.on('updated', () => {
      if (this.is_separated) {
        applyCoordinateExpressions(
          this.root.querySelector('.primary'),
          this.instance.start_at,
          moment(this.instance.start_at).endOf('date')
        );
        applyCoordinateExpressions(
          this.root.querySelector('.secondary'),
          moment(this.instance.end_at).startOf('date'),
          this.instance.end_at
        );
      }
      else {
        applyCoordinateExpressions(
          this.root.querySelector('.primary'),
          this.instance.start_at,
          this.instance.end_at
        );
      }
    });
  </script>
</reservations-filter-month-record>
