'''
  This file is part of the PyPhantomJS project.

  Copyright (C) 2011 James Roe <roejames12@hotmail.com>
  Copyright (C) 2011 Ariya Hidayat <ariya.hidayat@gmail.com>

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from PyQt4.QtCore import SIGNAL, QString, QUrl, QEventLoop, qDebug
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage

class WebPage(QWebPage):
    def __init__(self, parent = None):
        QWebPage.__init__(self, parent)

        self.parent = parent
        self.m_nextFileTag = QString()
        self.m_userAgent = QWebPage.userAgentForUrl(self, QUrl())

        if self.parent.m_verbose:
            self.connect(self.currentFrame(), SIGNAL('urlChanged(const QUrl&)'), self.handleFrameUrlChanged)
            self.connect(self, SIGNAL('linkClicked(const QUrl&)'), self.handleLinkClicked)

    def handleFrameUrlChanged(self, url):
        qDebug('URL Changed: %s' % url.toString())

    def handleLinkClicked(self, url):
        qDebug('URL Clicked: %s' % url.toString())

    def javaScriptAlert(self, webframe, msg):
        print 'JavaScript alert: %s' % msg

    def javaScriptConsoleMessage(self, message, lineNumber, sourceID):
        if sourceID:
            print sourceID + ':%s' % lineNumber + ' %s' % message.toUtf8()
        else:
            print message.toUtf8()

    def shouldInterruptJavaScript(self):
        QApplication.processEvents(QEventLoop.AllEvents, 42)
        return False

    def userAgentForUrl(self, url):
        return self.m_userAgent

    def chooseFile(self, webframe, suggestedFile):
        if self.m_nextFileTag in self.parent.m_upload_file:
            return self.parent.m_upload_file[self.m_nextFileTag]
        return QString()
