<reservations-thing>
  <h1>{ instance.name }</h1>
  <p>{ instance.remarks }</p>
  <img src={ instance.thumbnail } if={ instance.thumbnail } />

  <style scoped>
  :scope {
    display: block;
  }
  </style>

  <script>
    this.on('update', () => {
      this.state = opts.state;
      this.instance = this.state.thing;
    });
  </script>
</reservations-thing>
