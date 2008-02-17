
// Copyright (c) 2003 Ward Cunningham.
// Released under the terms of the GNU General Public License version 2 or later.

import java.applet.*;
import java.awt.*;
import java.io.*;
import java.net.*;
import java.util.*;

public class World extends Applet {
	
	Image world;		// background base map
	Dimension size;		// screen space for map
	Map nodes;		// stations read so far
	Frame frame;		// current movie frame
	String trouble; 	// last error message
	
	public void init () {
		world = getImage(getCodeBase(), "world2.gif");
		nodes = Collections.synchronizedMap(new HashMap());
		(new Thread(new Movie(), "Movie")).start();
	}
	
	public void paint (Graphics g) {
		size = getSize();
		g.drawImage(world, 0, 0, size.width, size.height, this);
                if (trouble != null) g.drawString(trouble, 10, 20);
		paintNodes(g);
		if (frame != null) frame.paint(g);
	}

	void paintNodes (Graphics g) {
		synchronized(nodes) { 		
			for (Iterator i=nodes.keySet().iterator(); i.hasNext();) {
				Node each = (Node)(nodes.get(i.next()));
				each.paint(g);
			}
		}	
	}
	
	void trouble (Throwable e) {
		trouble(e.getMessage());
	}

        void trouble (String s) {
                trouble = s;
                repaint();
        }

	
	static int xmin=-170, xmax=180;
	static int ymin=-50, ymax=95;

	Point scale (double lat, double lon) {
		int x = (int) ((lon-xmin)/(xmax-xmin) * size.width);
		int y = (int) ((1-(lat-ymin)/(ymax-ymin)) * size.height);
		return new Point(x, y);
	}

	void dot (Graphics g, Point p, int r) {
		g.setColor(Color.yellow);
		g.fillOval(p.x-r, p.y-r, 2*r, 2*r);
		g.setColor(Color.gray);
		g.drawOval(p.x-r, p.y-r, 2*r, 2*r);
	}		
	
	class Node {
		
		String name;
		double lat, lon;
		
		Node (String name, double lat, double lon){
			this.name = name;
			this.lat = lat;
			this.lon = lon;
		}
		
		Node (StringTokenizer tokens) {
			name = tokens.nextToken();
			lat = Double.parseDouble(tokens.nextToken());
			lon = Double.parseDouble(tokens.nextToken());		
		}
		
		void paint (Graphics g) {
			dot(g, origin(), 3);
		}

		Point origin () {
			return scale(lat, lon);
		}		
	}

	class Call {
		
		LinkedList stations = new LinkedList();
		
		Call (StringTokenizer tokens) {
			while(tokens.hasMoreTokens()) {
				stations.add(nodes.get(tokens.nextToken()));
			}
		}
		
		void paint (Graphics g) {
			Point from = center();
			g.setColor(stations.size()>2 ? Color.gray : Color.black);
			for (Iterator i = stations.iterator(); i.hasNext(); ) {
				Point to = ((Node)i.next()).origin();
				g.drawLine(from.x, from.y, to.x, to.y);
			}
		}
		
		Point center () {
			Point p = new Point(0,0);
			for (Iterator i = stations.iterator(); i.hasNext(); ) {
				Point q = ((Node)i.next()).origin();
				p.x += q.x;
				p.y += q.y;
			}
			p.x /= stations.size();
			p.y /= stations.size();
			return p;
		}	
	}

	class Frame {
		
		String time = null;
		LinkedList calls = new LinkedList();
		
		void paint (Graphics g) {
			for (Iterator i=calls.iterator(); i.hasNext();) {
				Call each = (Call)(i.next());
				each.paint(g);
			}		
			if (time != null) {
				Point sun = scale(75.0, sun(time));
				dot(g, sun, 10);
			}
		}
		
		double sun (String time) {
			int zulu = Integer.parseInt(time);
			double hours = zulu / 100;
			double mins = zulu % 100;
			return 180 - 360 * (hours/24 + mins/24/60);
		}
	}

	class Movie implements Runnable {
		
		BufferedReader input;
		LinkedList loop = new LinkedList();
		
		public void run () {
			open();
			sleep(); sleep();
                        try {
			while((frame=read()) != null) {
				loop.add(frame);
				repaint();
				sleep();
			}
			while (true) {
				for (Iterator i = loop.iterator(); i.hasNext(); ) {
					frame = (Frame)i.next();
					repaint();
					sleep();
				}
			}
                        } catch (Throwable e) {
                                trouble(e);
                        }
		}
		
		void sleep () {
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {	
				trouble(e);
			}
		}
		
		void open () {
			try {
				URL movie = new URL(getDocumentBase(), "movie.cgi");
				input = new BufferedReader(new InputStreamReader((InputStream) movie.getContent()));
			} catch (Exception e) {
				trouble(e);
			}
		}
		
		Frame read () {
			Frame next = new Frame();
			while(true) {
				String line = readLine();
				if (line == null) {
					return null;	// end of movie
				}
				StringTokenizer tokens = new StringTokenizer(line);
				if (tokens.countTokens()==0) {
					return next;	// end of frame
				}
				String type = tokens.nextToken();		
				if (type.equals("node")) {
					String number = tokens.nextToken();
					nodes.put(number, new Node(tokens));
				} else if (type.equals("call")) {
					next.calls.add(new Call(tokens));
				} else if (type.equals("time")) {
					next.time = tokens.nextToken();
				} else {
                                        trouble("don't know type: "+type);
                                }
			}
		}
		
		String readLine () {
			try {
				return input.readLine();
			} catch (IOException e) {
				trouble(e);
				return null;
			}			
		}
	}
}
