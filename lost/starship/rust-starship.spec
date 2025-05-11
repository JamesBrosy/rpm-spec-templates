#
# spec file for package rust-starship
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

%bcond check 1

%global debug_package %{nil}
%global crate starship

Name:           rust-starship
Version:        VERSION
Release:        1%{?dist}
Summary:        Minimal, blazing-fast, and infinitely customizable prompt for any shell! ☄🌌️

License:        ISC
# LICENSE.dependencies contains a full license breakdown
URL:            https://github.com/starship/starship
Source:         %{url}/archive/v%{version}/%{crate}-%{version}.tar.gz
# Automatically generated patch to strip dependencies and normalize metadata
Patch:          starship-fix-metadata-auto.diff

BuildRequires:  rust-packaging, git

%global _description %{expand:
Minimal, blazing-fast, and infinitely customizable prompt for any shell! ☄🌌️.}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}
License:        ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND (0BSD OR MIT OR Apache-2.0) AND Apache-2.0 AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR BSL-1.0 OR MIT) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR MIT OR Apache-2.0) AND BSD-3-Clause AND (CC0-1.0 OR MIT-0 OR Apache-2.0) AND ISC AND MIT AND (MIT AND Apache-2.0) AND (MIT OR Apache-2.0) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Zlib OR Apache-2.0) AND MPL-2.0 AND Unicode-3.0 AND Unlicense AND (Unlicense OR MIT) AND Zlib AND (Zlib OR Apache-2.0 OR MIT)

%description -n %{crate} %{_description}

%files       -n %{crate}
%license LICENSES
%license LICENSE.dependencies
%doc README.md
%{_bindir}/%{crate}

%prep
%autosetup -n %{crate}-%{version} -p1

%__cargo vendor
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
install -Dspm 0755 target/release/%{crate} -t %{buildroot}%{_bindir}

%if %{with check}
%check
%cargo_test
%endif

%changelog
* DATE Jo Carllyle <JamesBrosy@users.noreply.github.com>
- See Github for full changelog