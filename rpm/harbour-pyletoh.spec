# Prevent brp-python-bytecompile from running
%define __os_install_post %{___build_post}

Summary: Simple LeTOH controller
Name: harbour-pyletoh
Version: 0.6.0
Release: 1
Source: %{name}-%{version}.tar.gz
BuildArch: noarch
URL: https://github.com/datakurre/harbour-pyletoh
License: GPLv3
Group: System/GUI/Other
Requires: dbus-python3
Requires: python3-gobject
Requires: libsailfishapp-launcher
Requires: nemo-qml-plugin-dbus-qt5
Requires: pyotherside-qml-plugin-python3-qt5 >= 1.3.0
Requires: sailfishsilica-qt5
BuildRequires: systemd
BuildRequires: python3-base

%description
pyLeTOH is a simple controller for the Light emitting The Other Half

%changelog
* Sun Feb 22 2015 Asko Soukka <asko.soukka@iki.fi> - 0.6.0-1
- Feature: Animations (when background services are enabled)
* Wed Feb 4 2015 Asko Soukka <asko.soukka@iki.fi> - 0.5.0-1
- Feature: Turn lights on by incoming calls (similarly to notifications)
* Wed Feb 4 2015 Asko Soukka <asko.soukka@iki.fi> - 0.4.1-1
- Fix: UI for toggling notification background daemons on / off
* Tue Feb 3 2015 Asko Soukka <asko.soukka@iki.fi> - 0.4.0-1
- Feature: Save selected color
- Fix: Use python background daemons instead of QML d-bus bindings
* Thu Jan 29 2015 Asko Soukka <asko.soukka@iki.fi> - 0.2.1-1
- Feature: Pulley menu for turning LeTOH on / off
- Fix: Cover state to sync correctly with LeTOH state
* Thu Jan 29 2015 Asko Soukka <asko.soukka@iki.fi> - 0.2.0-1
- Feature: Cover action for toggling lights on / off)
- Feature: Turn lights on by notifications
- Feature: Turn lights off when closing notifications
* Tue Jan 27 2015 Asko Soukka <asko.soukka@iki.fi> - 0.1.18-1
- Fix: OBS based build
* Tue Jan 27 2015 Asko Soukka <asko.soukka@iki.fi> - 0.1.11-1
- First release

%prep
%setup -q

%build
pyvenv bootstrap
bootstrap/bin/pip install requires/dist/setuptools-12.0.5.tar.gz --upgrade
bootstrap/bin/pip install requires/dist/zc.buildout-2.3.1.tar.gz
bootstrap/bin/buildout bootstrap
python3 qml/buildout buildout:install-from-cache=true
rm -rf qml/buildout lib/zc.recipe*
cat qml/setup.py

%install
TARGET=%{buildroot}/%{_datadir}/%{name}
mkdir -p $TARGET
cp -rpv qml $TARGET/
cp -rpv lib $TARGET/
cp -rpv src $TARGET/

TARGET=%{buildroot}/%{_datadir}/applications
mkdir -p $TARGET
cp -rpv %{name}.desktop $TARGET/

TARGET=%{buildroot}/%{_datadir}/icons/hicolor/86x86/apps
mkdir -p $TARGET
cp -rpv %{name}.png $TARGET/

TARGET=%{buildroot}/%{_libdir}/systemd/user
mkdir -p $TARGET
cp -rpv *.service $TARGET/

%preun
su nemo -c "systemctl --user stop %{name}"
su nemo -c "systemctl --user stop %{name}-eavesdropper"
su nemo -c "systemctl --user --no-reload disable %{name}"
su nemo -c "systemctl --user --no-reload disable %{name}-eavesdropper"

%post
su nemo -c "systemctl --user --no-reload enable %{name}"
su nemo -c "systemctl --user --no-reload enable %{name}-eavesdropper"
su nemo -c "systemctl --user start %{name}"
su nemo -c "systemctl --user start %{name}-eavesdropper"
su nemo -c "systemctl --user daemon-reload"

%postun
su nemo -c "systemctl --user daemon-reload"

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_libdir}/systemd/user/%{name}.service
%{_libdir}/systemd/user/%{name}-eavesdropper.service
