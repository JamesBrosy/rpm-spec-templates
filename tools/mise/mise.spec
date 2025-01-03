#
# spec file for package mise
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

%global         _build_id_links none
%global         debug_package %{nil}
%global         pkgname mise

Name:           %{pkgname}
Version:        VERSION
Release:        1%{?dist}
Summary:        The front-end to your dev env

License:        MIT
URL:            https://github.com/jdx/%{pkgname}
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildRequires:  gcc, curl, openssl, openssl-devel, zlib, zlib-devel


%description
The front-end to your dev env

%package        bash-completion
Summary:        Bash completion for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)

%description    bash-completion
Bash command line completion support for %{name}.

%package        zsh-completion
Summary:        Zsh completion for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       zsh
Supplements:    (%{name} and zsh)

%description    zsh-completion
Zsh command line completion support for %{name}.

%package        fish-completion
Summary:        Fish completion for %{name}
Requires:       fish
Supplements:    (%{name} and fish)

%description fish-completion
Fish command line completion support for %{name}.

%prep
%autosetup

%build
# install toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
# fetch deps
cargo fetch --locked --target "$(rustc -vV | sed -n 's/host: //p')"
# build release
cargo build --offline --release --frozen
./target/release/%{pkgname} completion zsh > target/_%{pkgname}
./target/release/%{pkgname} completion bash > target/%{pkgname}
./target/release/%{pkgname} completion fish > target/%{pkgname}.fish
touch target/empty_file
cat << 'EOF' > target/%{pkgname}.sh
# Activate mise. See https://mise.jdx.dev/installing-mise.html#shells
eval "$(mise activate $(ps -p $$ -o comm=))"
EOF


%install
install -Dsm755 -T target/release/%{pkgname} %{buildroot}%{_bindir}/%{pkgname}
install -Dm644  -T man/man1/%{pkgname}.1     %{buildroot}%{_mandir}/man1/%{pkgname}.1
install -Dm644  -T target/_%{pkgname}        %{buildroot}%{_datadir}/zsh/site-functions/_%{pkgname}
install -Dm644  -T target/%{pkgname}         %{buildroot}%{_datadir}/bash-completion/completions/%{pkgname}
install -Dm644  -T target/%{pkgname}.fish    %{buildroot}%{_datadir}/fish/vendor_completions.d/%{pkgname}.fish
install -Dm644  -T target/empty_file         %{buildroot}/usr/lib/%{pkgname}/.disable-self-update
install -Dm644  -T target/%{pkgname}.sh      %{buildroot}%{_sysconfdir}/profile.d/%{pkgname}.sh


%files
%license LICENSE
%{_bindir}/%{pkgname}
%{_mandir}/man1/*
%dir /usr/lib/%{pkgname}
/usr/lib/%{pkgname}/.disable-self-update
%dir %{_sysconfdir}/profile.d
%{_sysconfdir}/profile.d/*

%files bash-completion
%{_datadir}/bash-completion/*

%files zsh-completion
%{_datadir}/zsh/*

%files fish-completion
%{_datadir}/fish/*


%changelog
* DATE Jeff Dickey <216188+jdx@users.noreply.github.com>
- See GitHub for full changelog
