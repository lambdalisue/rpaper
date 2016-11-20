<reservations-record>
  <span class="name">{ instance.name }</span>
  <span class="contact">{ instance.contact }</span>
  <span class="remarks">{ instance.remarks }</span>
  <span class="start_at">{ instance.start_at.format("kk:mm") }</span>
  <span class="end_at">{ instance.end_at.format("kk:mm") }</span>

  <style scoped>
    :scope {
      display: block;
      background-color: #aaa;
    }
  </style>

  <script>
    this.on('update', () => {
      this.instance = opts.instance;
    });
  </script>
</reservations-record>
