{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "from pyalgotrade import strategy\n",
    "from pyalgotrade.technical import ma\n",
    "from pyalgotrade.technical import cross\n",
    "\n",
    "\n",
    "class SMACrossOver(strategy.BacktestingStrategy):\n",
    "    def __init__(self, feed, instrument, smaPeriod):\n",
    "        super(SMACrossOver, self).__init__(feed)\n",
    "        self.__instrument = instrument\n",
    "        self.__position = None\n",
    "        # We'll use adjusted close values instead of regular close values.\n",
    "        self.setUseAdjustedValues(True)\n",
    "        self.__prices = feed[instrument].getPriceDataSeries()\n",
    "        self.__sma = ma.SMA(self.__prices, smaPeriod)\n",
    "\n",
    "    def getSMA(self):\n",
    "        return self.__sma\n",
    "\n",
    "    def onEnterCanceled(self, position):\n",
    "        self.__position = None\n",
    "\n",
    "    def onExitOk(self, position):\n",
    "        self.__position = None\n",
    "\n",
    "    def onExitCanceled(self, position):\n",
    "        # If the exit was canceled, re-submit it.\n",
    "        self.__position.exitMarket()\n",
    "\n",
    "    def onBars(self, bars):\n",
    "        # If a position was not opened, check if we should enter a long position.\n",
    "        if self.__position is None:\n",
    "            if cross.cross_above(self.__prices, self.__sma) > 0:\n",
    "                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())\n",
    "                # Enter a buy market order. The order is good till canceled.\n",
    "                self.__position = self.enterLong(self.__instrument, shares, True)\n",
    "        # Check if we have to exit the position.\n",
    "        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:\n",
    "            self.__position.exitMarket()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
