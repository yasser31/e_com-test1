document.querySelector('.dropdown-toggle').addEventListener('click', function () {
        document.querySelector('.dropdown-menu').classList.toggle('show');
      });
      document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('mouseover', function () {
          this.querySelector('.child-menu').style.display = 'block';
        });
        item.addEventListener('mouseout', function () {
          this.querySelector('.child-menu').style.display = 'none';
        });
      });
