Name:           sing-geoip
Version:        1.1
Release:        1%{?dist}
Summary:        GeoIP Database and Rule Sets for sing-box

License:        CC-BY-SA-4.0 GPL-3.0-or-later
URL:            https://github.com/SagerNet/%{name}
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  git
Requires:       sing-box
BuildArch:      noarch

%description
GeoIP Database and Rule Sets for sing-box

%package        db
Summary:        GeoIP Database for sing-box
Requires:       sing-box
BuildArch:      noarch

%description    db
GeoIP Database for sing-box

%package        rule-set
Summary:        GeoIP Rule Sets for sing-box
Requires:       sing-box
BuildArch:      noarch

%description    rule-set
GeoIP Rule Sets for sing-box


%prep
%autosetup


%build


%install
# install sing-geoip-db
git checkout release
install -Dm644 geoip*.db -t %{buildroot}%{_datadir}/sing-box/geoip-db
# install sing-geoip-rule-set
git checkout rule-set
install -Dm644 geoip-*.srs -t %{buildroot}%{_datadir}/sing-box/geoip-rule-set

git checkout main




%files
%license LICENSE

%files db
%{_datadir}/sing-box/geoip-db/*

%files rule-set
%{_datadir}/sing-box/geoip-rule-set/*


%changelog
%autochangelog
