#
# spec file for package vpndnshelper
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           vpndnshelper
Version:        0.0.1
Release:        0
Summary:        VPN DNS Helper
License:        GPL-2.0-only
Group:          Productivity/Networking/Other
URL:            https://github.com/frispete/%{name}
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.conf
Source2:        %{name}.service
BuildRequires:  dnsmasq
BuildRequires:  python3-setuptools
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(systemd)
Requires:       dnsmasq
Requires:       sysconfig-netconfig
Recommends:     NetworkManager
BuildArch:      noarch

%description
VPN DNS Helper is a tool, that allows local DNS server to coexist
with corporate VPN DNS server by adjusting the dnsmasq configuration
dynamically.

%prep
%setup -q

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/dnsmasq.d/%{name}.conf
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
mkdir -p %{buildroot}%{_sbindir}
ln -s service %{buildroot}/%{_sbindir}/rc%{name}

%pre
%service_add_pre %{name}.service

%preun
%service_del_preun %{name}.service

%post
%service_add_post %{name}.service

%postun
%service_del_postun %{name}.service

%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/dnsmasq.d/%{name}.conf
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%{_sbindir}/rc%{name}
%{python3_sitelib}/{,__pycache__/}%{name}*

%changelog
