#
# spec file for package eza
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

%bcond check 1

%global crate eza

Name:           rust-eza
Version:        VERSION
Release:        1%{?dist}
Summary:        Modern replacement for ls

License:        EUPL-1.2
URL:            https://github.com/eza-community/eza
Source:         %{url}/archive/v%{version}/%{crate}-%{version}.tar.gz
# Automatically generated patch to strip dependencies and normalize metadata
Patch:          eza-fix-metadata-auto.diff

BuildRequires:  cargo-rpm-macros >= 24 pandoc

%global _description %{expand:
A modern replacement for ls.}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}
License:        (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND EUPL-1.2 AND MIT AND (MIT OR Apache-2.0) AND (MIT OR Apache-2.0 OR CC0-1.0) AND (MIT OR Zlib OR Apache-2.0) AND MPL-2.0 AND Unicode-3.0 AND (Unlicense OR MIT)
# LICENSE.dependencies contains a full license breakdown

%description -n %{crate} %{_description}

%files       -n %{crate}
%license LICENSES/*.txt
%license LICENSE.dependencies
%doc CHANGELOG.md
%doc CODE_OF_CONDUCT.md
%doc CONTRIBUTING.md
%doc INSTALL.md
%doc README.md
%doc SECURITY.md
%doc TESTING.md
%{_bindir}/eza
%{_mandir}/man1/*
%{_mandir}/man5/*

%package        bash-completion
Summary:        Bash Completion for %{crate}
Group:          System/Shells
Requires:       %{crate} = %{version}
Supplements:    (%{crate} and bash-completion)
BuildArch:      noarch

%description    bash-completion
Bash command line completion support for %{crate}.

%files          bash-completion
%{_datadir}/bash-completion/completions/%{crate}

%package        zsh-completion
Summary:        Zsh Completion for %{crate}
Group:          System/Shells
Requires:       %{crate} = %{version}
Supplements:    (%{crate} and zsh)
BuildArch:      noarch

%description    zsh-completion
Zsh command line completion support for %{crate}.

%files          zsh-completion
%{_datadir}/zsh/site-functions/_%{crate}

%package        fish-completion
Summary:        Fish completion for %{crate}
Group:          System/Shells
Requires:       %{crate} = %{version}
Supplements:    (%{crate} and fish)
BuildArch:      noarch

%description    fish-completion
Fish command line completion support for %{crate}.

%files          fish-completion
%{_datadir}/fish/vendor_completions.d/%{crate}.fish

%prep
%autosetup -n %{crate}-%{version} -p1
%generate_buildrequires
%cargo_generate_buildrequires

%cargo_prep

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
%cargo_install

# Manpage
install -d -m 0755 %{buildroot}%{_mandir}/man1/
pandoc --standalone -f markdown -t man man/eza.1.md > %{buildroot}%{_mandir}/man1/eza.1

install -d -m 0755 %{buildroot}%{_mandir}/man5/
pandoc --standalone -f markdown -t man man/eza_colors.5.md > %{buildroot}%{_mandir}/man5/eza_colors.5
pandoc --standalone -f markdown -t man man/eza_colors-explanation.5.md > %{buildroot}%{_mandir}/man5/eza_colors-explanation.5

# Completion files
install -Dpm 0644 completions/bash/eza -t %{buildroot}/%{bash_completions_dir}/
install -Dpm 0644 completions/fish/eza.fish -t %{buildroot}/%{fish_completions_dir}/
install -Dpm 0644 completions/zsh/_eza -t %{buildroot}/%{zsh_completions_dir}/

%if %{with check}
%check
%cargo_test
%endif

%changelog
* DATE Jo Carllyle <JamesBrosy@users.noreply.github.com>
- See Github for full changelog