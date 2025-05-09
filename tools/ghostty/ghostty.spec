#
# spec file for package ghostty
#
# Copyright (c) 2024 Jo Carllyle
#

# Please submit bugfixes or comments via https://github.com/JamesBrosy/rpm-spec-templates
#

# Signing key from https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
%global public_key RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV
%global common_build_flags -Doptimize=ReleaseFast -Dcpu=baseline -Dpie=true -Dstrip=false -Dversion-string=%{version} %{?_smp_mflags}


Name:           ghostty
Version:        VERSION
Release:        1%{?dist}
Summary:        Cross-platform terminal emulator
License:        MIT
URL:            https://github.com/ghostty-org/ghostty
Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz.minisig
BuildRequires:  gobject-introspection
BuildRequires:  pandoc
BuildRequires:  pkgconfig
BuildRequires:  zig
BuildRequires:  zstd
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  python3-gobject
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  minisign
Requires:       ghostty-terminfo = %{version}

%description
Ghostty is a fast, feature-rich, and cross-platform terminal
emulator that uses platform-native UI and GPU acceleration.

%package        bash-completion
Summary:        Bash Completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)
BuildArch:      noarch

%description    bash-completion
Bash command-line completion support for %{name}.

%package        fish-completion
Summary:        Fish Completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}
Requires:       fish
Supplements:    (%{name} and fish)
BuildArch:      noarch

%description    fish-completion
Fish command-line completion support for %{name}.

%package        zsh-completion
Summary:        Zsh Completion for %{name}
Group:          System/Shells
Requires:       %{name} = %{version}
Requires:       zsh
Supplements:    (%{name} and zsh)
BuildArch:      noarch

%description    zsh-completion
Zsh command-line completion support for %{name}.

%package doc
Summary:        Documentation for %{name}
Group:          Documentation/HTML
BuildArch:      noarch

%description doc
This package provides documentation for %{name}

%package neovim
Summary:        Neovim syntax highlighting for %{name} data files
Requires:       %{name} = %{version}
Requires:       neovim
Supplements:    (%{name} and neovim)
BuildArch:      noarch

%description neovim
Optional files for syntax highlighting for %{name} data files in neovim.

%package vim
Summary:        Vim syntax highlighting for %{name} data files
Requires:       %{name} = %{version}
Requires:       neovim
Supplements:    (%{name} and vim)
BuildArch:      noarch

%description vim
Optional files for syntax highlighting for %{name} data files in vim.

%package        nautilus-extension
Summary:        Nautilus extension for ghostty
Requires:       %{name} = %{version}
Requires:       nautilus
%if 0%{?suse_version}
Requires:       python-nautilus-common-files
%else
Requires:       nautilus-python
%endif
Requires:       python3-gobject
Supplements:    (%{name} and nautilus)
BuildArch:      noarch

%description    nautilus-extension
Nautilus extension for ghostty.

%package        terminfo
Summary:        Terminfo files for ghostty
BuildArch:      noarch

%description    terminfo
Ghostty is a fast, feature-rich, and cross-platform terminal
emulator that uses platform-native UI and GPU acceleration.

This holds the terminfo files for ghostty.

%prep
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -P %{public_key}
%autosetup

%build
zig build %{common_build_flags}

%install
export DESTDIR=%{buildroot}
zig build %{common_build_flags} --prefix %{_prefix}

#Don't conflict with ncurses-term on F42 and up
%if 0%{?fedora} >= 42
rm -rf %{buildroot}%{_datadir}/terminfo/g/ghostty
%endif

%files
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/icons/hicolor/128x128/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/128x128@2/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/16x16/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/16x16@2/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/256x256/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/256x256@2/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/32x32/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/32x32@2/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/512x512/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/1024x1024/apps/com.mitchellh.ghostty.png
%dir %{_datadir}/icons/hicolor/128x128@2
%dir %{_datadir}/icons/hicolor/128x128@2/apps
%dir %{_datadir}/icons/hicolor/16x16@2
%dir %{_datadir}/icons/hicolor/16x16@2/apps
%dir %{_datadir}/icons/hicolor/256x256@2
%dir %{_datadir}/icons/hicolor/256x256@2/apps
%dir %{_datadir}/icons/hicolor/32x32@2
%dir %{_datadir}/icons/hicolor/32x32@2/apps

%dir %{_datadir}/ghostty
%dir %{_datadir}/ghostty/shell-integration
%{_datadir}/ghostty/shell-integration/elvish/
%{_datadir}/ghostty/themes/

%dir %{_datadir}/bat
%dir %{_datadir}/bat/syntaxes
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax

%dir %{_datadir}/kio
%dir %{_datadir}/kio/servicemenus
%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop

%files nautilus-extension
%{_datadir}/nautilus-python/extensions/ghostty.py

%files neovim
%{_datadir}/nvim/site/ftdetect/ghostty.vim
%{_datadir}/nvim/site/ftplugin/ghostty.vim
%{_datadir}/nvim/site/syntax/ghostty.vim
%{_datadir}/nvim/site/compiler/ghostty.vim
%dir %{_datadir}/nvim
%dir %{_datadir}/nvim/site
%dir %{_datadir}/nvim/site/ftdetect
%dir %{_datadir}/nvim/site/ftplugin
%dir %{_datadir}/nvim/site/syntax
%dir %{_datadir}/nvim/site/compiler/

%files doc
%dir %{_datadir}/ghostty/doc
%{_datadir}/ghostty/doc/ghostty.1.html
%{_datadir}/ghostty/doc/ghostty.1.md
%{_datadir}/ghostty/doc/ghostty.5.html
%{_datadir}/ghostty/doc/ghostty.5.md

%files bash-completion
%{_datadir}/bash-completion/completions/ghostty.bash
%{_datadir}/ghostty/shell-integration/bash/

%files fish-completion
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/ghostty/shell-integration/fish/

%files zsh-completion
%{_datadir}/zsh/site-functions/_ghostty
%{_datadir}/ghostty/shell-integration/zsh/

%files vim
%dir %{_datadir}/vim
%dir %{_datadir}/vim/vimfiles
%dir %{_datadir}/vim/vimfiles/ftdetect
%dir %{_datadir}/vim/vimfiles/ftplugin
%dir %{_datadir}/vim/vimfiles/syntax
%dir %{_datadir}/vim/vimfiles/compiler
%{_datadir}/vim/vimfiles/ftdetect/ghostty.vim
%{_datadir}/vim/vimfiles/ftplugin/ghostty.vim
%{_datadir}/vim/vimfiles/syntax/ghostty.vim
%{_datadir}/vim/vimfiles/compiler/ghostty.vim

%files terminfo
%if 0%{?fedora} < 42
%{_datadir}/terminfo/g/ghostty
%endif
%{_datadir}/terminfo/x/xterm-ghostty

%changelog
* DATE Mitchell Hashimoto <m@mitchellh.com>
- See GitHub for full changelog