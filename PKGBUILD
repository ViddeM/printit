# Maintainer: Vidar Magnusson <vprint@vidarmagnusson.com>

pkgname=vprint
pkgver=0.0.1
pkgrel=1
pkgdesc="Utility for printing at Chalmers University"
arch=("any")
url="https://github.com/viddem/vprint"
makedepends=("git")
depends=("python>=3" "python-requests" "python-setuptools" "python-pip")
source=("$pkgname-$pkgver::https://github.com/viddem/vprint.git")
sha256sums=("SKIP")

build() {
    ls
    cd "$pkgname-$pkgver"
    echo "-------------"
    ls 
    pip install ./
}

package() {
    cd "$pkgname-$pkgver"
    python setup install --prefix"/user" --root="${pkgdir}" --optimize=1 --skip-build
}